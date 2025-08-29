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
    global _client
    if _client is not None:
        return _client
    _client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    return _client


@pyscript_compile
def _internal_url() -> str | None:
    try:
        return network.get_url(hass, allow_external=False)
    except network.NoURLAvailableError:
        return None


@pyscript_compile
def _external_url() -> str | None:
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
    description: Tool for retrieving the conversation ID from cache.
    fields:
      chat_id:
        name: Chat ID
        description: The unique identifier of the chat to retrieve from cache.
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
    description: Tool for storing the conversation ID to cache.
    fields:
      chat_id:
        name: Chat ID
        description: The unique identifier of the chat to store in cache.
        required: true
        selector:
          text: {}
      conversation_id:
        name: Conversation ID
        description: The unique identifier of the conversation to store in cache.
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
    description: Tool for generating a unique, secure, URL-safe Webhook ID.
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
