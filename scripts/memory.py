import asyncio
import json
import re
import sqlite3
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import unicodedata

DB_PATH = Path("/config/memory.db")
RESULT_ENTITY = "sensor.memory_result"
TTL_MAX_DAYS = 3650
SEARCH_LIMIT_MAX = 50
NEAR_DISTANCE = 5

_DB_READY = False
_DB_READY_LOCK = threading.Lock()

result_entity_name = {
    "friendly_name": " ".join(
        word.capitalize() for word in RESULT_ENTITY.split(".")[-1].split("_")
    )
}


def _utcnow_iso() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _dt_from_iso(s: str) -> datetime | None:
    """Parse an ISO string into datetime; return None if invalid."""
    try:
        return datetime.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def _ensure_db() -> None:
    """Ensure database exists and tables/indices are created.

    Uses a short-lived connection to avoid leaving an idle connection open
    at import time.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA temp_store=MEMORY;")
        conn.execute("PRAGMA busy_timeout=3000;")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mem
            (
                key          TEXT PRIMARY KEY,
                value        TEXT NOT NULL,
                scope        TEXT NOT NULL,
                tags         TEXT NOT NULL,
                created_at   TEXT NOT NULL,
                last_used_at TEXT NOT NULL,
                ttl_at       TEXT
            );
            """
        )
        conn.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS mem_fts USING fts5(
                key, value, tags,
                content='mem',
                tokenize = 'unicode61 remove_diacritics 2'
            );
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_scope ON mem(scope);")
        conn.executescript(
            """
            CREATE TRIGGER IF NOT EXISTS mem_ai
                AFTER INSERT
                ON mem
            BEGIN
                INSERT INTO mem_fts(rowid, key, value, tags)
                VALUES (new.rowid,
                        new.key,
                        new.value || ' ' || REPLACE(REPLACE(new.value, 'đ', 'd'), 'Đ', 'D'),
                        new.tags || ' ' || REPLACE(REPLACE(new.tags, 'đ', 'd'), 'Đ', 'D'));
            END;

            CREATE TRIGGER IF NOT EXISTS mem_ad
                AFTER DELETE
                ON mem
            BEGIN
                INSERT INTO mem_fts(mem_fts, rowid) VALUES ('delete', old.rowid);
            END;

            CREATE TRIGGER IF NOT EXISTS mem_au
                AFTER UPDATE
                ON mem
            BEGIN
                INSERT INTO mem_fts(mem_fts, rowid) VALUES ('delete', old.rowid);
                INSERT INTO mem_fts(rowid, key, value, tags)
                VALUES (new.rowid,
                        new.key,
                        new.value || ' ' || REPLACE(REPLACE(new.value, 'đ', 'd'), 'Đ', 'D'),
                        new.tags || ' ' || REPLACE(REPLACE(new.tags, 'đ', 'd'), 'Đ', 'D'));
            END;
            """
        )
        conn.execute("PRAGMA optimize;")
        conn.commit()


def _ensure_db_once(force: bool = False) -> None:
    """Ensure the database schema exists once per runtime."""
    global _DB_READY
    if force:
        _DB_READY = False
    if _DB_READY and DB_PATH.exists():
        return
    with _DB_READY_LOCK:
        if force:
            _DB_READY = False
        if not _DB_READY or not DB_PATH.exists():
            _ensure_db()
            _DB_READY = True


def _normalize_value(s: str) -> str:
    """Normalize a text value for storage (NFC)."""
    if s is None:
        return ""
    return unicodedata.normalize("NFC", str(s))


def _normalize_tags(s: str) -> str:
    """Normalize tags: NFC, replace commas with spaces, collapse whitespace."""
    base = unicodedata.normalize("NFC", str(s)) if s is not None else ""
    base = base.replace(",", " ")
    return " ".join(base.split()).strip()


def _normalize_key(s: str) -> str:
    """Normalize a key to [a-z0-9_], lowercase, no accents."""
    if s is None:
        return ""
    s = str(s).strip().lower()
    t = unicodedata.normalize("NFD", s)
    filtered_chars = []
    for ch in t:
        if unicodedata.category(ch) != "Mn":
            filtered_chars.append(ch)
    t = "".join(filtered_chars)
    t = t.replace("đ", "d")
    t = re.sub(r"[^a-z0-9_]", "_", t)
    t = re.sub(r"_+", "_", t).strip("_")
    return t


def _tokenize_query(q: str) -> list[str]:
    """Tokenize a free-text query into simple word tokens for FTS.

    - Lowercase, strip diacritics via tokenizer (handled by FTS), but here we
      just extract word characters to avoid MATCH syntax issues.
    - Returns a list of tokens; empty list if none.
    """
    if not q:
        return []
    return re.findall(r"[A-Za-z0-9_]+", str(q).lower())


def _near_distance_for_tokens(n: int) -> int:
    """Compute dynamic NEAR distance based on token count."""
    if n <= 1:
        return 0
    val = 2 * n - 1
    if val < 3:
        val = 3
    if val > NEAR_DISTANCE:
        val = NEAR_DISTANCE
    return val


def _build_fts_queries(raw_query: str) -> list[str]:
    """Build a list of FTS5 MATCH query variants to improve recall.

    Strategy (ordered by priority):
    - PHRASE: exact phrase (highest precision when user typed a phrase)
    - NEAR: tokens appear within proximity (high relevance, dynamic distance)
    - AND: all tokens must appear (relevant but looser than NEAR)
    - OR*: any token with prefix match (broad recall)
    - RAW: the original raw query as a last option
    """
    tokens = _tokenize_query(raw_query)
    variants = []

    if tokens:
        # 1) PHRASE exact order (if 2+ tokens)
        if len(tokens) >= 2:
            phrase = " ".join(tokens)
            variants.append(f'"{phrase}"')

        # 2) NEAR across all tokens (if 2+ tokens)
        if len(tokens) >= 2:
            near_inner = " ".join(tokens)
            near_dist = _near_distance_for_tokens(len(tokens))
            variants.append(f"NEAR({near_inner}, {near_dist})")

        # 3) AND of all tokens (or single token)
        if len(tokens) == 1:
            variants.append(tokens[0])
        else:
            variants.append(" AND ".join(tokens))

        # 4) OR with prefix match to broaden recall
        or_tokens = [f"{t}*" for t in tokens]
        variants.append(" OR ".join(or_tokens))

    # 5) RAW as very last resort if provided
    rq = (raw_query or "").strip()
    if rq:
        variants.append(rq)

    # Deduplicate while preserving order
    seen = set()
    out = []
    for v in variants:
        if v not in seen:
            out.append(v)
            seen.add(v)
    return out


def _purge_if_expired(cur: sqlite3.Cursor, key: str) -> bool:
    """Delete key if TTL has passed; return True if deleted."""
    row = cur.execute("SELECT ttl_at FROM mem WHERE key=?", (key,)).fetchone()
    if not row:
        return False
    ttl_at = row[0]
    if ttl_at:
        dt = _dt_from_iso(ttl_at)
        if dt and datetime.now(timezone.utc) > dt:
            cur.execute("DELETE FROM mem WHERE key=?", (key,))
            return True
    return False


def _set_result(state_value: str = "ok", **attrs: Any) -> None:
    """Set result sensor state and attributes."""
    attrs.update(result_entity_name)
    state.set(RESULT_ENTITY, value=state_value, new_attributes=attrs)


def _reset_db_ready() -> None:
    """Mark the cached DB-ready flag as stale so the next call rebuilds."""
    global _DB_READY
    with _DB_READY_LOCK:
        _DB_READY = False


def _memory_set_db_sync(
    key_norm: str,
    value_norm: str,
    scope_norm: str,
    tags_norm: str,
    now_iso: str,
    ttl_at: str | None,
) -> bool:
    """Persist a memory record, retrying once if schema objects are missing."""
    for attempt in range(2):
        try:
            _ensure_db_once(force=attempt == 1)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO mem(key, value, scope, tags, created_at, last_used_at, ttl_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(key) DO UPDATE SET value=excluded.value,
                                                   scope=excluded.scope,
                                                   tags=excluded.tags,
                                                   last_used_at=excluded.last_used_at,
                                                   ttl_at=excluded.ttl_at
                    """,
                    (
                        key_norm,
                        value_norm,
                        scope_norm,
                        tags_norm,
                        now_iso,
                        now_iso,
                        ttl_at,
                    ),
                )
                conn.commit()
            return True
        except sqlite3.OperationalError:
            _reset_db_ready()
            if attempt == 0:
                continue
            raise
    return False


def _memory_get_db_sync(key_norm: str) -> tuple[str, dict[str, Any] | None]:
    """Fetch a memory by key, updating access time and handling expiry."""
    for attempt in range(2):
        try:
            _ensure_db_once(force=attempt == 1)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                expired = _purge_if_expired(cur, key_norm)
                if expired:
                    conn.commit()
                    return "expired", None
                row = cur.execute(
                    """
                    SELECT key, value, scope, tags, created_at, last_used_at, ttl_at
                    FROM mem
                    WHERE key = ?;
                    """,
                    (key_norm,),
                ).fetchone()
                if not row:
                    return "not_found", None
                last_used_iso = _utcnow_iso()
                cur.execute(
                    "UPDATE mem SET last_used_at=? WHERE key=?",
                    (last_used_iso, key_norm),
                )
                conn.commit()
            result = {
                "key": row[0],
                "value": row[1],
                "scope": row[2],
                "tags": row[3],
                "created_at": row[4],
                "last_used_at": last_used_iso,
                "ttl_at": row[6],
            }
            return "ok", result
        except sqlite3.OperationalError:
            _reset_db_ready()
            if attempt == 0:
                continue
            raise
    return "error", None


def _memory_search_db_sync(query: str, limit: int) -> list[dict[str, Any]]:
    """Run the primary search query, returning matching memory rows."""
    for attempt in range(2):
        try:
            _ensure_db_once(force=attempt == 1)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute(
                    "DELETE FROM mem WHERE ttl_at IS NOT NULL AND ttl_at < ?",
                    (_utcnow_iso(),),
                )
                conn.commit()

                found_by_key: dict[str, tuple] = {}
                total_rows: list[tuple] = []
                match_variants = _build_fts_queries(query)

                for mv in match_variants:
                    if len(found_by_key) >= limit:
                        break
                    try:
                        fetched = cur.execute(
                            """
                            SELECT DISTINCT m.key,
                                            m.value,
                                            m.scope,
                                            m.tags,
                                            m.created_at,
                                            m.last_used_at,
                                            m.ttl_at,
                                            bm25(mem_fts) AS rank
                            FROM mem m
                                     JOIN mem_fts ON m.key = mem_fts.key
                            WHERE mem_fts MATCH ?
                            ORDER BY rank, m.last_used_at DESC
                            LIMIT ?;
                            """,
                            (mv, limit),
                        ).fetchall()
                    except sqlite3.Error:
                        continue

                    for row in fetched:
                        key = row[0]
                        if key not in found_by_key:
                            found_by_key[key] = row
                            total_rows.append(row)
                        if len(found_by_key) >= limit:
                            break

                if not total_rows:
                    like_q = f"%{query}%"
                    total_rows = cur.execute(
                        """
                        SELECT DISTINCT m.key, m.value, m.scope, m.tags, m.created_at, m.last_used_at, m.ttl_at
                        FROM mem m
                        WHERE m.value LIKE ?
                           OR m.tags LIKE ?
                           OR m.key LIKE ?
                        ORDER BY m.last_used_at DESC
                        LIMIT ?;
                        """,
                        (like_q, like_q, like_q, limit),
                    ).fetchall()
            results: list[dict[str, Any]] = []
            for row in total_rows:
                results.append(
                    {
                        "key": row[0],
                        "value": row[1],
                        "scope": row[2],
                        "tags": row[3],
                        "created_at": row[4],
                        "last_used_at": row[5],
                        "ttl_at": row[6],
                    }
                )
            return results
        except sqlite3.OperationalError:
            _reset_db_ready()
            if attempt == 0:
                continue
            raise
    return []


def _memory_forget_db_sync(key_norm: str) -> int:
    """Delete a memory row by key and return the number of rows removed."""
    for attempt in range(2):
        try:
            _ensure_db_once(force=attempt == 1)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM mem WHERE key=?", (key_norm,))
                rowcount = getattr(cur, "rowcount", -1)
                deleted = rowcount if rowcount and rowcount > 0 else 0
                conn.commit()
            return deleted
        except sqlite3.OperationalError:
            _reset_db_ready()
            if attempt == 0:
                continue
            raise
    return 0


def _memory_purge_expired_db_sync() -> int:
    """Remove expired rows from the main table and report how many were purged."""
    for attempt in range(2):
        try:
            _ensure_db_once(force=attempt == 1)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute(
                    "DELETE FROM mem WHERE ttl_at IS NOT NULL AND ttl_at < ?",
                    (_utcnow_iso(),),
                )
                rowcount = getattr(cur, "rowcount", -1)
                removed = rowcount if rowcount and rowcount > 0 else 0
                conn.commit()
            return removed
        except sqlite3.OperationalError:
            _reset_db_ready()
            if attempt == 0:
                continue
            raise
    return 0


def _memory_reindex_fts_db_sync() -> tuple[int, int]:
    """Rebuild the FTS index, returning counts before and after the rebuild."""
    for attempt in range(2):
        try:
            _ensure_db_once(force=attempt == 1)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                try:
                    cur.execute("SELECT COUNT(*) FROM mem_fts")
                    before = cur.fetchone()[0]
                except sqlite3.Error:
                    before = 0

                cur.execute("DROP TABLE IF EXISTS mem_fts")
                cur.execute(
                    """
                    CREATE VIRTUAL TABLE mem_fts USING fts5(
                        key, value, tags,
                        content='mem',
                        tokenize = 'unicode61 remove_diacritics 2'
                    );
                    """
                )

                cur.executescript(
                    """
                    DROP TRIGGER IF EXISTS mem_ai;
                    DROP TRIGGER IF EXISTS mem_ad;
                    DROP TRIGGER IF EXISTS mem_au;
                    CREATE TRIGGER mem_ai AFTER INSERT ON mem BEGIN
                        INSERT INTO mem_fts(rowid, key, value, tags)
                        VALUES (
                            new.rowid,
                            new.key,
                            new.value || ' ' || REPLACE(REPLACE(new.value,'đ','d'),'Đ','D'),
                            new.tags  || ' ' || REPLACE(REPLACE(new.tags, 'đ','d'),'Đ','D')
                        );
                    END;
                    CREATE TRIGGER mem_ad AFTER DELETE ON mem BEGIN
                        INSERT INTO mem_fts(mem_fts, rowid) VALUES('delete', old.rowid);
                    END;
                    CREATE TRIGGER mem_au AFTER UPDATE ON mem BEGIN
                        INSERT INTO mem_fts(mem_fts, rowid) VALUES('delete', old.rowid);
                        INSERT INTO mem_fts(rowid, key, value, tags)
                        VALUES (
                            new.rowid,
                            new.key,
                            new.value || ' ' || REPLACE(REPLACE(new.value,'đ','d'),'Đ','D'),
                            new.tags  || ' ' || REPLACE(REPLACE(new.tags, 'đ','d'),'Đ','D')
                        );
                    END;
                    """
                )

                cur.execute("INSERT INTO mem_fts(mem_fts) VALUES('rebuild')")
                cur.execute("SELECT COUNT(*) FROM mem_fts")
                after = cur.fetchone()[0]
                conn.commit()
            return before, after
        except sqlite3.OperationalError:
            _reset_db_ready()
            if attempt == 0:
                continue
            raise
    return 0, 0


def _memory_health_check_db_sync() -> tuple[int, int, int]:
    """Return basic health counts (total, expired, FTS rows) for diagnostics."""
    for attempt in range(2):
        try:
            _ensure_db_once(force=attempt == 1)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM mem")
                rows = cur.fetchone()[0]
                now_iso = _utcnow_iso()
                cur.execute(
                    "SELECT COUNT(*) FROM mem WHERE ttl_at IS NOT NULL AND ttl_at < ?",
                    (now_iso,),
                )
                expired = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM mem_fts")
                fts_rows = cur.fetchone()[0]
            return rows, expired, fts_rows
        except sqlite3.OperationalError:
            _reset_db_ready()
            if attempt == 0:
                continue
            raise
    return 0, 0, 0


async def _memory_set_db(
    key_norm: str,
    value_norm: str,
    scope_norm: str,
    tags_norm: str,
    now_iso: str,
    ttl_at: str | None,
) -> bool:
    return await asyncio.to_thread(
        _memory_set_db_sync,
        key_norm,
        value_norm,
        scope_norm,
        tags_norm,
        now_iso,
        ttl_at,
    )


async def _memory_get_db(key_norm: str) -> tuple[str, dict[str, Any] | None]:
    return await asyncio.to_thread(_memory_get_db_sync, key_norm)


async def _memory_search_db(query: str, limit: int) -> list[dict[str, Any]]:
    return await asyncio.to_thread(_memory_search_db_sync, query, limit)


async def _memory_forget_db(key_norm: str) -> int:
    return await asyncio.to_thread(_memory_forget_db_sync, key_norm)


async def _memory_purge_expired_db() -> int:
    return await asyncio.to_thread(_memory_purge_expired_db_sync)


async def _memory_reindex_fts_db() -> tuple[int, int]:
    return await asyncio.to_thread(_memory_reindex_fts_db_sync)


async def _memory_health_check_db() -> tuple[int, int, int]:
    return await asyncio.to_thread(_memory_health_check_db_sync)


@service(supports_response="only")
async def memory_set(
    key: str, value: str, scope: str = "user", ttl_days: int = 180, tags: str = ""
):
    """
    yaml
    name: Memory Set
    description: Create or update a memory entry with optional TTL and tags.
    fields:
      key:
        name: Key
        description: Unique key of the entry.
        required: true
        example: "car_parking_slot"
        selector:
          text:
      value:
        name: Value
        description: Value to store (string or JSON-encoded structure).
        required: true
        example: "Column B2E9"
        selector:
          text:
      scope:
        name: Scope
        description: Arbitrary grouping label for organization.
        required: false
        default: user
        example: user
        selector:
          text:
      ttl_days:
        name: TTL (days)
        description: Days until expiration; 0 disables TTL.
        required: false
        default: 180
        example: 30
        selector:
          number:
            min: 0
            max: 3650
            mode: box
      tags:
        name: Tags
        description: Optional space-separated tags for improved search.
        required: false
        default: ""
        example: "car parking slot"
        selector:
          text:
    """
    key_norm = _normalize_key(key)
    if not key_norm or value is None:
        _set_result("error", op="set", key=key_norm or "", error="key_or_value_missing")
        log.error("memory_set: missing key or value")
        return {
            "status": "error",
            "op": "set",
            "key": key_norm or "",
            "error": "key_or_value_missing",
        }

    try:
        ttl_i = int(ttl_days)
    except (TypeError, ValueError):
        ttl_i = 0
    if ttl_i < 0:
        ttl_i = 0
    if ttl_i > TTL_MAX_DAYS:
        ttl_i = TTL_MAX_DAYS

    try:
        scope_norm = str(scope).strip() or "user"
        value_norm = _normalize_value(value)
        tags_norm = _normalize_tags(tags)

        now = datetime.now(timezone.utc)
        now_iso = now.isoformat()
        ttl_at = (now + timedelta(days=ttl_i)).isoformat() if ttl_i else None

        ok_db = await _memory_set_db(
            key_norm=key_norm,
            value_norm=value_norm,
            scope_norm=scope_norm,
            tags_norm=tags_norm,
            now_iso=now_iso,
            ttl_at=ttl_at,
        )

        if not ok_db:
            return {
                "status": "error",
                "op": "set",
                "key": key_norm,
                "scope": scope_norm,
                "error": "memory_set_db returned False",
            }

        _set_result(
            "ok",
            op="set",
            key=key_norm,
            scope=scope_norm,
            ttl_at=ttl_at,
            value=value_norm,
        )
        event.fire("memory_set_done", key=key_norm, scope=scope_norm, ttl_at=ttl_at)
        return {
            "status": "ok",
            "op": "set",
            "key": key_norm,
            "scope": scope_norm,
            "ttl_at": ttl_at,
            "value": value_norm,
        }
    except Exception as e:
        log.error(f"memory_set failed: {e}")
        _set_result("error", op="set", key=key_norm, error=str(e))
        return {"status": "error", "op": "set", "key": key_norm, "error": str(e)}


@service(supports_response="only")
async def memory_get(key: str):
    """
    yaml
    name: Memory Get
    description: Get a memory entry by key and update its last_used_at.
    fields:
      key:
        name: Key
        description: Key to fetch.
        required: true
        example: "car_parking_slot"
        selector:
          text:
    """
    key_norm = _normalize_key(key)
    if not key_norm:
        _set_result("error", op="get", key=key or "", error="key_missing")
        return {
            "status": "error",
            "op": "get",
            "key": key or "",
            "error": "key_missing",
        }

    try:
        status, payload = await _memory_get_db(key_norm)
    except Exception as e:
        log.error(f"memory_get failed: {e}")
        _set_result("error", op="get", key=key_norm, error=str(e))
        return {"status": "error", "op": "get", "key": key_norm, "error": str(e)}

    if status == "expired":
        _set_result("not_found", op="get", key=key_norm, expired=True)
        return {
            "status": "not_found",
            "op": "get",
            "key": key_norm,
            "expired": True,
        }

    if status == "not_found":
        _set_result("not_found", op="get", key=key_norm)
        return {"status": "not_found", "op": "get", "key": key_norm}

    res = payload or {}
    _set_result("ok", op="get", **res)
    event.fire("memory_get_result", **res)
    return {"status": "ok", "op": "get", **res}


@service(supports_response="only")
async def memory_search(query: str, limit: int = 5):
    """
    yaml
    name: Memory Search
    description: Search entries across key/value/tags using FTS; falls back to LIKE if MATCH fails.
    fields:
      query:
        name: Query
        description: FTS search query.
        required: true
        example: "parking slot"
        selector:
          text:
      limit:
        name: Limit
        description: Maximum number of results to return.
        required: false
        default: 5
        example: 5
        selector:
          number:
            min: 1
            max: 50
            mode: box
    """
    if not query:
        _set_result("error", op="search", query=query or "", error="query_missing")
        return {
            "status": "error",
            "op": "search",
            "query": query or "",
            "error": "query_missing",
        }

    try:
        lim = int(limit)
    except (TypeError, ValueError):
        lim = 5
    if lim < 1:
        lim = 1
    if lim > SEARCH_LIMIT_MAX:
        lim = SEARCH_LIMIT_MAX

    try:
        results = await _memory_search_db(query, lim)
    except Exception as e:
        log.error(f"memory_search failed: {e}")
        _set_result("error", op="search", query=query, error=str(e))
        return {"status": "error", "op": "search", "query": query, "error": str(e)}

    _set_result(
        "ok",
        op="search",
        query=query,
        count=len(results),
        results=json.dumps(results),
    )
    event.fire("memory_search_result", query=query, count=len(results))
    return {
        "status": "ok",
        "op": "search",
        "query": query,
        "count": len(results),
        "results": results,
    }


@service(supports_response="only")
async def memory_forget(key: str):
    """
    yaml
    name: Memory Forget
    description: Delete a memory entry by key and remove it from the FTS index.
    fields:
      key:
        name: Key
        description: Key to delete.
        required: true
        example: "car_parking_slot"
        selector:
          text:
    """
    key_norm = _normalize_key(key)
    if not key_norm:
        _set_result("error", op="forget", key=key or "", error="key_missing")
        return {
            "status": "error",
            "op": "forget",
            "key": key or "",
            "error": "key_missing",
        }
    try:
        deleted = await _memory_forget_db(key_norm)
    except Exception as e:
        log.error(f"memory_forget failed: {e}")
        _set_result("error", op="forget", key=key_norm, error=str(e))
        return {"status": "error", "op": "forget", "key": key_norm, "error": str(e)}

    _set_result("ok", op="forget", key=key_norm, deleted=deleted)
    event.fire("memory_forget_done", key=key_norm, deleted=deleted)
    return {"status": "ok", "op": "forget", "key": key_norm, "deleted": deleted}


@service(supports_response="only")
async def memory_purge_expired():
    """
    yaml
    name: Memory Purge Expired
    description: Remove expired records; FTS triggers maintain the index.
    """
    try:
        removed = await _memory_purge_expired_db()
    except Exception as e:
        log.error(f"memory_purge_expired failed: {e}")
        _set_result("error", op="purge_expired", error=str(e))
        return {"status": "error", "op": "purge_expired", "error": str(e)}

    _set_result("ok", op="purge_expired", removed=removed)
    event.fire("memory_purge_done", removed=removed)
    return {"status": "ok", "op": "purge_expired", "removed": removed}


@service(supports_response="only")
async def memory_reindex_fts():
    """
    yaml
    name: Memory Reindex FTS
    description: Rebuild the FTS index from the main table. Useful when mem_fts is empty or out of sync.
    """
    try:
        before, after = await _memory_reindex_fts_db()
    except Exception as e:
        log.error(f"memory_reindex_fts failed: {e}")
        _set_result("error", op="reindex_fts", error=str(e))
        return {"status": "error", "op": "reindex_fts", "error": str(e)}

    _set_result("ok", op="reindex_fts", removed=before, inserted=after)
    event.fire("memory_reindex_done", removed=before, inserted=after)
    return {
        "status": "ok",
        "op": "reindex_fts",
        "removed": before,
        "inserted": after,
    }


@time_trigger("startup")
@service(supports_response="only")
async def memory_health_check():
    """
    yaml
    name: Memory Health Check
    description: Run a quick health check (counts, expired, FTS rows), update the sensor, and return details.
    """
    try:
        rows, expired, fts_rows = await _memory_health_check_db()
        ts = _utcnow_iso()
        _set_result(
            "idle",
            op="health",
            db_path=DB_PATH,
            rows=rows,
            expired=expired,
            fts_rows=fts_rows,
            ts=ts,
        )
        log.info(
            f"memory.py health: rows={rows}, expired={expired}, fts_rows={fts_rows}"
        )
        return {
            "status": "ok",
            "op": "health",
            "db_path": DB_PATH,
            "rows": rows,
            "expired": expired,
            "fts_rows": fts_rows,
            "ts": ts,
        }
    except Exception as e:
        log.error(f"memory_health_check failed: {e}")
        _set_result("error", op="health", error=str(e))
        return {"status": "error", "op": "health", "error": str(e)}


@time_trigger("cron(0 3 * * *)")
async def memory_daily_housekeeping():
    """Daily housekeeping: purge expired items and clean FTS index."""
    try:
        await memory_purge_expired()
    except Exception as e:
        log.error(f"memory_daily_housekeeping failed: {e}")
