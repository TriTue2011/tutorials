import asyncio
import mimetypes
import os
import secrets
from pathlib import Path
from typing import Any

import aiofiles
import aiohttp
from homeassistant.helpers import network

DIRECTORY = "/media/zalo"
TOKEN = pyscript.config.get("zalo_bot_token")

_session: aiohttp.ClientSession | None = None

if not TOKEN:
    raise ValueError("Zalo bot token is missing")


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
async def _download_file(session: aiohttp.ClientSession, url: str) -> str | None:
    async with session.get(url) as resp:
        resp.raise_for_status()
        content = await resp.read()
        content_type = resp.headers.get("Content-Type", "")
        ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ""
        file_name = Path(url).name
        if not Path(file_name).suffix and ext:
            file_name += ext
        file_path = os.path.join(DIRECTORY, file_name)
        await _write_file(file_path, content)
        return file_path


@pyscript_compile
async def _send_message(
    session: aiohttp.ClientSession, chat_id: str, message: str
) -> dict[str, Any]:
    url = f"https://bot-api.zapps.me/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message[:2000]}
    async with session.post(url, json=payload) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


@pyscript_compile
async def _get_webhook_info(session: aiohttp.ClientSession) -> dict[str, Any]:
    url = f"https://bot-api.zapps.me/bot{TOKEN}/getWebhookInfo"
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


@pyscript_compile
async def _set_webhook(
    session: aiohttp.ClientSession, base_url: str, webhook_id: str
) -> dict[str, Any]:
    url = f"https://bot-api.zapps.me/bot{TOKEN}/setWebhook"
    params = {
        "url": f"{base_url}/api/webhook/{webhook_id}",
        "secret_token": secrets.token_urlsafe(),  # A required parameter but ignored by Home Assistant.
    }
    async with session.post(url, json=params) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


@pyscript_compile
async def _delete_webhook(session: aiohttp.ClientSession) -> dict[str, Any]:
    url = f"https://bot-api.zapps.me/bot{TOKEN}/deleteWebhook"
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


@pyscript_compile
async def _get_updates(
    session: aiohttp.ClientSession, timeout: int = 30
) -> dict[str, Any]:
    url = f"https://bot-api.zapps.me/bot{TOKEN}/getUpdates"
    async with session.post(url, json={"timeout": timeout}) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


@pyscript_compile
async def _get_me(session: aiohttp.ClientSession) -> dict[str, Any]:
    url = f"https://bot-api.zapps.me/bot{TOKEN}/getMe"
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


@pyscript_compile
async def _send_chat_action(
    session: aiohttp.ClientSession, chat_id: str, action: str = "typing"
) -> dict[str, Any]:
    url = f"https://bot-api.zapps.me/bot{TOKEN}/sendChatAction"
    params = {"chat_id": chat_id, "action": action}
    async with session.post(url, json=params) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


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
async def send_zalo_message(chat_id: str, message: str) -> dict[str, Any]:
    """
    yaml
    name: Send Zalo Message
    description: Tool for sending messages directly to Zalo users via Zalo bot.
    fields:
      chat_id:
        name: Chat ID
        description: The unique identifier of the target chat where the message will be sent.
        required: true
        selector:
          text: {}
      message:
        name: Message
        description: The message content to be delivered to the target Zalo chat.
        required: true
        selector:
          text: {}
    """
    if not all([chat_id, message]):
        return {"error": "Missing one or more required arguments: chat_id, message"}
    try:
        session = await _ensure_session()
        response = await _send_message(session, chat_id, message)
        if not response:
            return {"error": "Failed to send message"}
        return response
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="only")
async def get_zalo_file(url: str) -> dict[str, Any]:
    """
    yaml
    name: Get Zalo File
    description: Tool for retrieving and downloading media files directly from Zalo messages or channels.
    fields:
      url:
        name: URL
        description: The URL of the media file to be downloaded.
        required: true
        selector:
          text: {}
    """
    if not url:
        return {"error": "Missing a required argument: url"}
    try:
        session = await _ensure_session()
        await _ensure_dir(DIRECTORY)

        file_path = await _download_file(session, url)
        if not file_path:
            return {"error": "Unable to download the file from Zalo."}

        mime_type, encoding = mimetypes.guess_file_type(file_path)
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
async def get_zalo_webhook() -> dict[str, Any]:
    """
    yaml
    name: Get Zalo Bot Webhook
    description: Tool for retrieving Zalo bot Webhook information.
    """
    try:
        session = await _ensure_session()
        return await _get_webhook_info(session)
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="only")
async def set_zalo_webhook(webhook_id: str | None = None) -> dict[str, Any]:
    """
    yaml
    name: Set Zalo Bot Webhook
    description: Tool for configuring Zalo bot Webhook information.
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
async def delete_zalo_webhook() -> dict[str, Any]:
    """
    yaml
    name: Delete Zalo Bot Webhook
    description: Tool for removing Zalo bot Webhook information.
    """
    try:
        session = await _ensure_session()
        return await _delete_webhook(session)
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="only")
async def get_zalo_updates(timeout: int = 30) -> dict[str, Any]:
    """
    yaml
    name: Get Zalo Updates
    description: Tool for getting Zalo messages updates.
    fields:
      timeout:
        name: Timeout
        description: Time to wait for a response from the Zalo.
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
async def get_zalo_bot_info() -> dict[str, Any]:
    """
    yaml
    name: Get Zalo Bot Information
    description: Tool for getting Zalo bot basic information.
    """
    try:
        session = await _ensure_session()
        return await _get_me(session)
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}


@service(supports_response="only")
async def send_zalo_chat_action(chat_id: str) -> dict[str, Any]:
    """
    yaml
    name: Send Zalo Chat Action
    description: Tool for sending chat action directly to Zalo users via Zalo bot.
    fields:
      chat_id:
        name: Chat ID
        description: The unique identifier of the target chat where the message will be sent.
        required: true
        selector:
          text: {}
    """
    if not chat_id:
        return {"error": "Missing a required argument: chat_id"}
    try:
        session = await _ensure_session()
        response = await _send_chat_action(session, chat_id)
        if not response:
            return {"error": "Failed to send message"}
        return response
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}
