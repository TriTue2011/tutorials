import asyncio
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any

TTL = 300  # The Conversation ID retention period in Home Assistant is set to a fixed 5 minutes of idle time and cannot be modified.
DB_PATH = Path("/config/cache.db")

_CACHE_READY = False
_CACHE_READY_LOCK = threading.Lock()


def _ensure_cache_db() -> None:
    """Create the cache database directory, SQLite file, and schema if they do not already exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA temp_store=MEMORY;")
        conn.execute("PRAGMA busy_timeout=3000;")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cache_entries
            (
                key        TEXT PRIMARY KEY,
                value      TEXT    NOT NULL,
                expires_at INTEGER NOT NULL
            )
            """
        )
        conn.commit()


def _ensure_cache_db_once(force: bool = False) -> None:
    """Ensure the cache database exists, optionally forcing a rebuild."""
    global _CACHE_READY
    if force:
        _CACHE_READY = False
    if _CACHE_READY and DB_PATH.exists():
        return
    with _CACHE_READY_LOCK:
        if force:
            _CACHE_READY = False
        if not _CACHE_READY or not DB_PATH.exists():
            _ensure_cache_db()
            _CACHE_READY = True


def _reset_cache_ready() -> None:
    """Mark the cache database schema as stale so it will be recreated."""
    global _CACHE_READY
    with _CACHE_READY_LOCK:
        _CACHE_READY = False


def _cache_prepare_db_sync(force: bool = False) -> bool:
    """Ensure the cache database is ready for use."""
    _ensure_cache_db_once(force=force)
    return True


def _cache_get_sync(key: str) -> str | None:
    """Retrieve the cached value for a key, pruning expired rows first."""
    for attempt in range(2):
        try:
            _ensure_cache_db_once(force=attempt == 1)
            now = int(time.time())
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute("DELETE FROM cache_entries WHERE expires_at <= ?", (now,))
                conn.commit()
                cur.execute(
                    """
                    SELECT value
                    FROM cache_entries
                    WHERE key = ?
                      AND expires_at > ?
                    """,
                    (key, now),
                )
                row = cur.fetchone()
            return row["value"] if row else None
        except sqlite3.OperationalError:
            _reset_cache_ready()
            if attempt == 0:
                continue
            raise
    return None


def _cache_set_sync(key: str, value: str, ttl_seconds: int) -> bool:
    """Persist a cache entry with the provided TTL and prune expired records."""
    for attempt in range(2):
        try:
            _ensure_cache_db_once(force=attempt == 1)
            now = int(time.time())
            expires_at = now + ttl_seconds
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM cache_entries WHERE expires_at <= ?", (now,))
                cur.execute(
                    """
                    INSERT INTO cache_entries (key, value, expires_at)
                    VALUES (?, ?, ?)
                    ON CONFLICT(key) DO UPDATE SET value      = excluded.value,
                                                   expires_at = excluded.expires_at
                    """,
                    (key, value, expires_at),
                )
                conn.commit()
            return True
        except sqlite3.OperationalError:
            _reset_cache_ready()
            if attempt == 0:
                continue
            raise
    return False


def _cache_delete_sync(key: str) -> int:
    """Remove the cache entry identified by key if it exists."""
    for attempt in range(2):
        try:
            _ensure_cache_db_once(force=attempt == 1)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM cache_entries WHERE key = ?", (key,))
                deleted = cur.rowcount if cur.rowcount is not None else 0
                conn.commit()
            return max(deleted, 0)
        except sqlite3.OperationalError:
            _reset_cache_ready()
            if attempt == 0:
                continue
            raise
    return 0


async def _cache_prepare_db(force: bool = False) -> bool:
    """Ensure the cache database is ready for use."""
    return await asyncio.to_thread(_cache_prepare_db_sync, force)


async def _cache_get(key: str) -> str | None:
    """Retrieve the cached value for a key, pruning expired rows first."""
    return await asyncio.to_thread(_cache_get_sync, key)


async def _cache_set(key: str, value: str, ttl_seconds: int) -> bool:
    """Persist a cache entry with the provided TTL and prune expired records."""
    return await asyncio.to_thread(_cache_set_sync, key, value, ttl_seconds)


async def _cache_delete(key: str) -> int:
    """Remove the cache entry identified by key if it exists."""
    return await asyncio.to_thread(_cache_delete_sync, key)


@time_trigger("startup")
async def initialize_cache_db() -> None:
    """Run once at startup to create the cache database and schema before services execute."""
    await _cache_prepare_db(force=True)


@service(supports_response="only")
async def memory_cache_get(key: str) -> dict[str, Any]:
    """
    yaml
    name: Memory Cache Get
    description: Fetch a cached value for a given key.
    fields:
      key:
        name: Key
        description: Identifier for the cached entry.
        required: true
        selector:
          text:
    """
    if not key:
        return {
            "status": "error",
            "op": "get",
            "error": "Missing a required argument: key",
        }
    try:
        value = await _cache_get(key)
        if value:
            return {
                "status": "ok",
                "op": "get",
                "key": key,
                "value": value,
            }
        return {
            "status": "error",
            "op": "get",
            "key": key,
            "error": "not_found",
        }
    except Exception as error:
        return {
            "status": "error",
            "op": "get",
            "key": key,
            "error": f"An unexpected error occurred during processing: {error}",
        }


@service(supports_response="only")
async def memory_cache_forget(key: str) -> dict[str, Any]:
    """
    yaml
    name: Memory Cache Forget
    description: Remove a cached entry if it exists.
    fields:
      key:
        name: Key
        description: Identifier for the cached entry.
        required: true
        selector:
          text:
    """
    if not key:
        return {
            "status": "error",
            "op": "forget",
            "error": "Missing a required argument: key",
        }
    try:
        deleted = await _cache_delete(key)
        return {
            "status": "ok",
            "op": "forget",
            "key": key,
            "deleted": deleted,
        }
    except Exception as error:
        return {
            "status": "error",
            "op": "forget",
            "key": key,
            "error": f"An unexpected error occurred during processing: {error}",
        }


@service(supports_response="only")
async def memory_cache_set(
    key: str,
    value: str,
    ttl_seconds: int | None = None,
) -> dict[str, Any]:
    """
    yaml
    name: Memory Cache Set
    description: Store a value in cache for a given key.
    fields:
      key:
        name: Key
        description: Identifier for the cached entry.
        required: true
        selector:
          text:
      value:
        name: Value
        description: Value to cache for the provided key.
        required: true
        selector:
          text:
      ttl_seconds:
        name: TTL Seconds
        description: Optional override for the entry's time to live (defaults to TTL constant).
        selector:
          number:
            min: 1
            max: 2592000
            mode: box
    """
    ttl = ttl_seconds if ttl_seconds is not None and ttl_seconds > 0 else TTL
    stored_value = str(value)
    try:
        success = await _cache_set(key, stored_value, ttl)
        if not success:
            return {
                "status": "error",
                "op": "set",
                "key": key,
                "value": stored_value,
                "error": "cache_set returned False",
            }
        return {
            "status": "ok",
            "op": "set",
            "key": key,
            "value": stored_value,
            "ttl": ttl,
        }
    except Exception as error:
        return {
            "status": "error",
            "op": "set",
            "key": key,
            "error": f"An unexpected error occurred during processing: {error}",
        }
