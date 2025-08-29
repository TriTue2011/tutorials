import asyncio
import mimetypes
import os
import secrets
from typing import Any

import aiofiles
import aiohttp
from homeassistant.helpers import network

TTL = 15  # Cache retention period (minutes)
DIRECTORY = "/media/telegram"
TOKEN = pyscript.config.get("telegram_bot_token")

_session: aiohttp.ClientSession | None = None

if not TOKEN:
    raise ValueError("Telegram bot token is missing")


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
async def _get_file(session: aiohttp.ClientSession, file_id: str) -> str | None:
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


@pyscript_compile
async def _send_message(
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
async def _set_webhook(
    session: aiohttp.ClientSession, base_url: str, webhook_id: str
) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    params = {
        "url": f"{base_url}/api/webhook/{webhook_id}",
        "drop_pending_updates": True,
    }
    async with session.post(url, json=params) as resp:
        resp.raise_for_status()
        return await resp.json()


@pyscript_compile
async def _delete_webhook(session: aiohttp.ClientSession) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
    params = {"drop_pending_updates": True}
    async with session.post(url, json=params) as resp:
        resp.raise_for_status()
        return await resp.json()


@pyscript_compile
async def _get_updates(
    session: aiohttp.ClientSession, timeout: int = 30
) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": timeout}
    async with session.post(url, json=params) as resp:
        resp.raise_for_status()
        return await resp.json()


@pyscript_compile
async def _get_me(session: aiohttp.ClientSession) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json()


@pyscript_compile
async def _send_chat_action(
    session: aiohttp.ClientSession,
    chat_id: int | str,
    message_thread_id: int | None = None,
    action: str = "typing",
) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{TOKEN}/sendChatAction"
    params = {
        "chat_id": chat_id,
        "action": action,
    }
    if message_thread_id:
        params["message_thread_id"] = message_thread_id
    async with session.post(url, json=params) as resp:
        resp.raise_for_status()
        return await resp.json()


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
async def send_telegram_message(
    chat_id: str,
    message: str,
    reply_to_message_id: int | None = None,
    message_thread_id: int | None = None,
) -> dict[str, Any]:
    """
    yaml
    name: Send Telegram Message
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
        response = await _send_message(
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
async def get_telegram_file(file_id: str) -> dict[str, Any]:
    """
    yaml
    name: Get Telegram File
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

        online_file_path = await _get_file(session, file_id)
        if not online_file_path:
            return {"error": "Unable to retrieve the file_path from Telegram."}

        content = await _download_file(session, online_file_path)
        if not content:
            return {"error": "Unable to download the file from Telegram."}

        file_name = os.path.basename(online_file_path)
        file_path = os.path.join(DIRECTORY, file_name)
        await _write_file(file_path, content)
        mime_type, encoding = mimetypes.guess_file_type(file_name)
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
        external_url = _external_url()
        if not external_url:
            return {
                "error": "The external Home Assistant URL is not found or incorrect."
            }
        session = await _ensure_session()
        response = await _set_webhook(session, external_url, webhook_id)
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
        return await _delete_webhook(session)
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="only")
async def get_telegram_updates(timeout: int = 30) -> dict[str, Any]:
    """
    yaml
    name: Get Telegram Updates
    description: Tool for getting Telegram messages updates.
    fields:
      timeout:
        name: Timeout
        description: Time to wait for a response from the Telegram.
        selector:
          number:
            min: 30
            max: 60
            step: 1
        default: 30
    """
    try:
        session = await _ensure_session()
        return await _get_updates(session, timeout=timeout)
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="only")
async def get_telegram_bot_info() -> dict[str, Any]:
    """
    yaml
    name: Get Telegram Bot Basic Information
    description: Tool for getting Telegram bot basic information.
    """
    try:
        session = await _ensure_session()
        return await _get_me(session)
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="only")
async def send_telegram_chat_action(
    chat_id: str,
    message_thread_id: int | None = None,
) -> dict[str, Any]:
    """
    yaml
    name: Send Telegram Chat Action
    description: Tool for sending chat action directly to Telegram users via Telegram bot.
    fields:
      chat_id:
        name: Chat ID
        description: The unique identifier of the target chat where the chat action will be sent.
        required: true
        selector:
          text: {}
      message_thread_id:
        name: Message Thread ID
        description: The unique identifier of the specific message thread (topic) where the chat action will be sent.
        selector:
          text: {}
    """
    if not chat_id:
        return {"error": "Missing a required argument: chat_id"}
    try:
        session = await _ensure_session()
        response = await _send_chat_action(session, chat_id, message_thread_id)
        if not response:
            return {"error": "Failed to send message"}
        return response
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}
