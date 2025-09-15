import secrets
from typing import Any

import redis.asyncio as redis
from homeassistant.helpers import network

TTL = 300  # The Conversation ID retention period in Home Assistant is set to a fixed 5 minutes of idle time and cannot be modified.
REDIS_HOST = pyscript.config.get("redis_host")
REDIS_PORT = pyscript.config.get("redis_port")

_client: redis.Redis | None = None

if not all([REDIS_HOST, REDIS_PORT]):
    raise ValueError("You need to configure your Redis host and port")


@pyscript_compile
def _redis() -> redis.Redis:
    """Return a shared Redis client (lazy-initialized).

    Uses host/port from pyscript config and `decode_responses=True` so values
    are handled as text. Keeps a module-level singleton for reuse.

    Returns:
        A connected `redis.Redis` client instance.
    """
    global _client
    if _client is not None:
        return _client
    _client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    return _client


@pyscript_compile
def _internal_url() -> str | None:
    """Get the internal Home Assistant URL if available.

    Returns:
        Internal URL string or None when not configured/available.
    """
    try:
        return network.get_url(hass, allow_external=False)
    except network.NoURLAvailableError:
        return None


@pyscript_compile
def _external_url() -> str | None:
    """Get the external HTTPS Home Assistant URL if available.

    The URL is fetched with `allow_internal=False`, `allow_ip=False`,
    `require_ssl=True`, and `require_standard_port=True` to ensure a
    publicly reachable, secure address suitable for webhooks.

    Returns:
        External URL string or None when not configured/available.
    """
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


@service(supports_response="only")
async def conversation_id_fetcher(chat_id: str) -> dict[str, Any]:
    """
    yaml
    name: Conversation ID Fetcher
    description: Fetch a cached conversation ID for a given chat.
    fields:
      chat_id:
        name: Chat ID
        description: ID of the conversation (user or group).
        required: true
        selector:
          text: {}
    """
    if not chat_id:
        return {"error": "Missing a required argument: chat_id"}
    try:
        cached = _redis()
        response = await cached.get(chat_id)
        return {"conversation_id": response}
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="optional")
async def conversation_id_setter(
    chat_id: str, conversation_id: str
) -> dict[str, Any] | None:
    """
    yaml
    name: Conversation ID Setter
    description: Store a conversation ID in cache (TTL ~5 minutes of idle).
    fields:
      chat_id:
        name: Chat ID
        description: ID of the conversation (user or group).
        required: true
        selector:
          text: {}
      conversation_id:
        name: Conversation ID
        description: Conversation ID to cache for the chat.
        required: true
        selector:
          text: {}
    """
    if not all([chat_id, conversation_id]):
        return {
            "error": "Missing one or more required arguments: chat_id, conversation_id"
        }
    try:
        cached = _redis()
        await cached.set(chat_id, conversation_id, ex=TTL)
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


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
