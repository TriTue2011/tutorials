import asyncio
import secrets
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any

from homeassistant.helpers import network

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


def _cache_prune_expired_sync(now: int | None = None) -> int:
    """Delete expired entries and return the number of rows removed."""
    now_ts = now if now is not None else int(time.time())
    for attempt in range(2):
        try:
            _ensure_cache_db_once(force=attempt == 1)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute(
                    "DELETE FROM cache_entries WHERE expires_at <= ?", (now_ts,)
                )
                removed = cur.rowcount if cur.rowcount is not None else 0
                conn.commit()
            return max(removed, 0)
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


async def _cache_prune_expired(now: int | None = None) -> int:
    """Delete expired entries and return the number of rows removed."""
    return await asyncio.to_thread(_cache_prune_expired_sync, now)


def _internal_url() -> str | None:
    """Return the internal Home Assistant URL, or None when it cannot be resolved."""
    try:
        return network.get_url(hass, allow_external=False)
    except network.NoURLAvailableError:
        return None


def _external_url() -> str | None:
    """Return the external HTTPS Home Assistant URL when configured and reachable."""
    try:
        return network.get_url(
            hass,
            allow_internal=False,
            allow_ip=False,
            require_ssl=True,
            require_standard_port=True,
        )
    except network.NoURLAvailableError:
        return None


@time_trigger("startup")
async def initialize_cache_db() -> None:
    """Run once at startup to create the cache database and schema before services execute."""
    await _cache_prepare_db(force=True)


@time_trigger("cron(15 3 * * *)")
async def cleanup_expired_cache() -> None:
    """Remove expired cache entries daily at 03:15 so the SQLite file stays compact."""
    await _cache_prepare_db(force=False)
    await _cache_prune_expired(int(time.time()))


@service(supports_response="only")
async def conversation_id_fetcher(chat_id: str) -> dict[str, Any]:
    """
    yaml
    name: Conversation ID Fetcher
    description: Fetch a cached conversation ID for a given chat if one exists.
    fields:
      chat_id:
        name: Chat ID
        description: Unique identifier of the conversation (user or group).
        required: true
        selector:
          text: {}
    """
    if not chat_id:
        return {
            "status": "error",
            "op": "get",
            "error": "Missing a required argument: chat_id",
        }
    try:
        conversation_id = await _cache_get(chat_id)
        return {
            "status": "ok",
            "op": "get",
            "chat_id": chat_id,
            "conversation_id": conversation_id,
        }
    except Exception as error:
        return {
            "status": "error",
            "op": "get",
            "error": f"An unexpected error occurred during processing: {error}",
        }


@service(supports_response="only")
async def conversation_id_setter(chat_id: str, conversation_id: str) -> dict[str, Any]:
    """
    yaml
    name: Conversation ID Setter
    description: Store a conversation ID in cache with a five minutes idle timeout.
    fields:
      chat_id:
        name: Chat ID
        description: Unique identifier of the conversation (user or group).
        required: true
        selector:
          text: {}
      conversation_id:
        name: Conversation ID
        description: Identifier to cache for the conversation.
        required: true
        selector:
          text: {}
    """
    if not all([chat_id, conversation_id]):
        return {
            "status": "error",
            "op": "set",
            "error": "Missing one or more required arguments: chat_id, conversation_id",
        }
    try:
        success = await _cache_set(chat_id, conversation_id, TTL)
        if not success:
            return {
                "status": "error",
                "op": "set",
                "chat_id": chat_id,
                "conversation_id": conversation_id,
                "error": "cache_set returned False",
            }
        return {
            "status": "ok",
            "op": "set",
            "chat_id": chat_id,
            "conversation_id": conversation_id,
        }
    except Exception as error:
        return {
            "status": "error",
            "op": "set",
            "error": f"An unexpected error occurred during processing: {error}",
        }


@service(supports_response="only")
def generate_webhook_id() -> dict[str, Any]:
    """
    yaml
    name: Generate Webhook ID
    description: Generate a unique URL-safe webhook ID and sample URLs.
    """
    webhook_id = secrets.token_urlsafe()
    internal_url = _internal_url()
    external_url = _external_url()
    response = {"webhook_id": webhook_id}
    if internal_url:
        response["sample_internal_url"] = f"{internal_url}/api/webhook/{webhook_id}"
    else:
        response["sample_internal_url"] = (
            "The internal Home Assistant URL is not found."
        )
    if external_url:
        response["sample_external_url"] = f"{external_url}/api/webhook/{webhook_id}"
    else:
        response["sample_external_url"] = (
            "The external Home Assistant URL is not found or incorrect."
        )
    return response
