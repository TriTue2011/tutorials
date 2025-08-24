import asyncio
import mimetypes
import os
import secrets
from datetime import timedelta
from typing import Any

import aiofiles
import aiohttp
import redis.asyncio as redis

TTL = 15  # Cache retention period (minutes)
DIRECTORY = "/media/telegram"
TOKEN = pyscript.config.get("telegram_bot_token")
REDIS_HOST = pyscript.config.get("redis_host")
REDIS_PORT = pyscript.config.get("redis_port")

_session: aiohttp.ClientSession | None = None

if not TOKEN:
    raise ValueError("Telegram bot token is missing")

if not all([REDIS_HOST, REDIS_PORT]):
    raise ValueError("You need to configure your Redis host and port")

cached = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@pyscript_compile
async def _ensure_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60))
    return _session


@pyscript_compile
async def _ensure_dir(path: str) -> None:
    await asyncio.to_thread(os.makedirs, path, exist_ok=True)


@pyscript_compile
async def _write_file(path: str, content: bytes) -> None:
    async with aiofiles.open(path, "wb") as f:
        await f.write(content)


@pyscript_compile
async def _get_file_path(session: aiohttp.ClientSession, file_id: str) -> str | None:
    url = f"https://api.telegram.org/bot{TOKEN}/getFile"
    async with session.post(url, json={"file_id": file_id}) as resp:
        resp.raise_for_status()
        data = await resp.json()
    return data.get("result", {}).get("file_path")


@pyscript_compile
async def _download_file(
    session: aiohttp.ClientSession, file_path: str
) -> bytes | None:
    url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.read()


async def _send_text(
    session: aiohttp.ClientSession,
    chat_id: int | str,
    message: str,
    reply_to_message_id: int | None = None,
    message_thread_id: int | None = None,
) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message[:4096]}
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id
    if message_thread_id:
        payload["message_thread_id"] = message_thread_id
    async with session.post(url, json=payload) as resp:
        resp.raise_for_status()
        return await resp.json()


@pyscript_compile
async def _get_webhook_info(session: aiohttp.ClientSession) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json()


@pyscript_compile
async def _set_webhook_info(
    session: aiohttp.ClientSession, base_url: str, webhook_id: str
) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    params = {"url": f"{base_url}/api/webhook/{webhook_id}"}
    async with session.post(url, json=params) as resp:
        resp.raise_for_status()
        return await resp.json()


@pyscript_compile
async def _delete_webhook_info(session: aiohttp.ClientSession) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json()


@service(supports_response="only")
async def telegram_message_handle_tool(
    chat_id: str,
    message: str,
    reply_to_message_id: int | None = None,
    message_thread_id: int | None = None,
) -> dict[str, Any]:
    """
    yaml
    name: Telegram Message Handle Tool
    description: Tool for sending messages directly to Telegram users via Telegram bot.
    fields:
      chat_id:
        name: Chat ID
        description: The unique identifier of the target chat where the message will be sent.
        required: true
        selector:
          text: {}
      message:
        name: Message
        description: The message content to be delivered to the target Telegram chat.
        required: true
        selector:
          text: {}
      reply_to_message_id:
        name: Reply To Message ID
        description: The unique identifier of the original message you want to reply to.
        selector:
          text: {}
      message_thread_id:
        name: Message Thread ID
        description: The unique identifier of the specific message thread (topic) where the message will be sent.
        selector:
          text: {}
    """
    if not all([chat_id, message]):
        return {"error": "Missing one or more required arguments: chat_id, message"}
    try:
        session = await _ensure_session()
        response = await _send_text(
            session,
            chat_id,
            message,
            reply_to_message_id=reply_to_message_id,
            message_thread_id=message_thread_id,
        )
        if not response:
            return {"error": "Failed to send message"}
        return response
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="only")
async def telegram_media_handle_tool(file_id: str) -> dict[str, Any]:
    """
    yaml
    name: Telegram Media Handle Tool
    description: Tool for retrieving and downloading media files directly from Telegram messages or channels.
    fields:
      file_id:
        name: File ID
        description: The unique identifier of the media file to be downloaded.
        required: true
        selector:
          text: {}
    """
    if not file_id:
        return {"error": "Missing a required argument: file_id"}
    try:
        session = await _ensure_session()
        await _ensure_dir(DIRECTORY)

        online_file_path = await _get_file_path(session, file_id)
        if not online_file_path:
            return {"error": "Unable to retrieve the file_path from Telegram."}

        content = await _download_file(session, online_file_path)
        if not content:
            return {"error": "Unable to download the file from Telegram."}

        (mime_type, encoding) = mimetypes.guess_file_type(online_file_path)
        file_name = os.path.basename(online_file_path)
        file_path = os.path.join(DIRECTORY, file_name)
        await _write_file(file_path, content)
        file_path = file_path.replace(
            "/media/", "/local/"
        )  # Change to public access path
        response: dict[str, Any] = {"file_path": file_path, "mime_type": mime_type}
        support_file_types = (
            "image/",
            "video/",
            "audio/",
            "text/",
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml",
        )
        if mime_type and mime_type.startswith(support_file_types):
            response["supported"] = True
        else:
            response["supported"] = False
        return response
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


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
        await cached.set(chat_id, conversation_id)
        await cached.expire(chat_id, timedelta(minutes=TTL))
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="only")
def generate_webhook_id() -> dict[str, Any]:
    """
    yaml
    name: Generate Webhook ID
    description: Tool for generating a unique, secure, URL-safe Webhook ID.
    """
    return {"webhook_id": secrets.token_urlsafe()}


@service(supports_response="only")
async def get_telegram_webhook() -> dict[str, Any]:
    """
    yaml
    name: Retrieve Telegram Bot Webhook URL
    description: Tool for retrieving Telegram bot Webhook information.
    """
    try:
        session = await _ensure_session()
        return await _get_webhook_info(session)
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="only")
async def set_telegram_webhook(webhook_id: str | None = None) -> dict[str, Any]:
    """
    yaml
    name: Configure Telegram Bot Webhook URL
    description: Tool for configuring Telegram bot Webhook information.
    fields:
      webhook_id:
        name: Webhook ID
        description: Enter a custom Webhook ID, or leave the field blank to have one generated automatically.
        selector:
          text: {}
    """
    try:
        if not webhook_id:
            webhook_id = secrets.token_urlsafe()
        base_url = hass.config.external_url
        if not base_url:
            return {
                "error": "Public Home Assistant URL not found. Please check under System - Network settings."
            }
        session = await _ensure_session()
        response = await _set_webhook_info(session, base_url, webhook_id)
        if isinstance(response, dict) and response.get("ok"):
            response["webhook_id"] = webhook_id
        return response
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="only")
async def delete_telegram_webhook() -> dict[str, Any]:
    """
    yaml
    name: Delete Telegram Bot Webhook URL
    description: Tool for removing Telegram bot Webhook information.
    """
    try:
        session = await _ensure_session()
        return await _delete_webhook_info(session)
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}
