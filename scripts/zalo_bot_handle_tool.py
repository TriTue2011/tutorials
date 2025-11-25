import asyncio
import mimetypes
import os
import secrets
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import aiofiles
import aiohttp
from homeassistant.helpers import network

DIRECTORY = "/media/zalo"
WWW_DIRECTORY = "/config/www/zalo"
TOKEN = pyscript.config.get("zalo_bot_token")

_session: aiohttp.ClientSession | None = None

if not TOKEN:
    raise ValueError("Zalo bot token is missing")


def _to_media_path(path: str) -> str:
    """Normalize Home Assistant media source path to /media/ prefix.

    Converts leading "local/" to "/media/". Leaves other paths unchanged but
    validates that they resolve to a path inside /media/ to prevent traversal.

    Args:
        path: Input file path from UI or config.

    Returns:
        Normalized absolute path beginning with "/media/".

    Raises:
        ValueError: If the resolved path is outside the allowed /media directory.
    """
    if path.startswith("local/"):
        path = "/media/" + path.removeprefix("local/")

    p = Path(path)
    if not p.is_absolute():
        p = Path("/media") / p

    try:
        resolved_path = p.resolve()
    except OSError:
        resolved_path = Path(os.path.abspath(str(p)))

    media_root = Path("/media").resolve()
    if media_root not in resolved_path.parents and resolved_path != media_root:
        raise ValueError(
            f"Security Error: Access to '{path}' (resolved to '{resolved_path}') "
            "is denied. Path must be inside /media."
        )

    return str(resolved_path)


def _to_relative_path(path: str) -> str:
    """Convert a /media/ path to Home Assistant local/ media source path.

    Converts leading "/media/" to "local/". Leaves other paths unchanged.

    Args:
        path: Absolute media path.

    Returns:
        Path with leading "local/" when applicable.
    """
    if path.startswith("/media/"):
        return "local/" + path.removeprefix("/media/")
    return path


async def _ensure_session() -> aiohttp.ClientSession:
    """Create or reuse a shared aiohttp session.

    Returns:
        An open `aiohttp.ClientSession` with a default timeout.
    """
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300))
    return _session


async def _ensure_dir(path: str) -> None:
    """Ensure a directory exists, creating it if missing.

    Args:
        path: Directory path to create if it does not exist.
    """
    await asyncio.to_thread(os.makedirs, path, exist_ok=True)


async def _cleanup_old_files(directory: str, days: int = 30) -> None:
    """Delete files in the directory older than the specified number of days."""
    now = time.time()
    cutoff = now - (days * 86400)

    def _cleanup_sync() -> None:
        if not os.path.exists(directory):
            return
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    t = os.path.getmtime(file_path)
                    if t < cutoff:
                        os.remove(file_path)
            except Exception:
                pass

    await asyncio.to_thread(_cleanup_sync)


async def _download_file(session: aiohttp.ClientSession, url: str) -> str | None:
    """Download a file from a given URL and save it under DIRECTORY (streaming).

    Args:
        session: Shared aiohttp session.
        url: Direct URL to the file to download.

    Returns:
        Full file path of the saved file, or None on failure.
    """
    try:
        async with session.get(url) as resp:
            resp.raise_for_status()
            content_type = resp.headers.get("Content-Type", "")
            ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ""

            # Use safe filename from URL or default, then append unique token
            parsed_url = urlparse(url)
            original_name = Path(parsed_url.path).name
            if not Path(original_name).suffix and ext:
                original_name += ext

            base, extension = os.path.splitext(original_name)
            # Construct unique filename: name_timestamp_random.ext
            file_name = f"{base}_{int(time.time())}_{secrets.token_hex(4)}{extension}"

            file_path = os.path.join(DIRECTORY, file_name)

            async with aiofiles.open(file_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(4096):
                    await f.write(chunk)

            return file_path
    except Exception:
        return None


async def _send_message(
    session: aiohttp.ClientSession, chat_id: str, message: str
) -> dict[str, Any]:
    """Send a text message to a Zalo chat.

    Args:
        session: Shared aiohttp session.
        chat_id: Target chat identifier on Zalo.
        message: Message text (truncated to ~2000 chars).

    Returns:
        Zalo API JSON response as a dict.
    """
    url = f"https://bot-api.zapps.me/bot{TOKEN}/sendMessage"
    text = message
    if len(text) > 2000:
        text = text[:1997] + "..."
    payload = {"chat_id": chat_id, "text": text}
    async with session.post(url, json=payload) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


async def _send_photo(
    session: aiohttp.ClientSession,
    chat_id: str,
    photo_url: str,
    caption: str | None = None,
) -> dict[str, Any]:
    """Send a photo to Zalo by public URL.

    Args:
        session: Shared aiohttp session.
        chat_id: Target chat identifier on Zalo.
        photo_url: Publicly accessible image URL.
        caption: Optional caption string.

    Returns:
        Zalo API JSON response as a dict.
    """
    url = f"https://bot-api.zapps.me/bot{TOKEN}/sendPhoto"
    payload: dict[str, Any] = {"chat_id": chat_id, "photo": photo_url}
    if caption:
        payload["caption"] = caption
    async with session.post(url, json=payload) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


async def _get_webhook_info(session: aiohttp.ClientSession) -> dict[str, Any]:
    """Retrieve current Zalo bot webhook information.

    Args:
        session: Shared aiohttp session.

    Returns:
        Zalo API JSON response as a dict.
    """
    url = f"https://bot-api.zapps.me/bot{TOKEN}/getWebhookInfo"
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


async def _set_webhook(
    session: aiohttp.ClientSession, base_url: str, webhook_id: str
) -> dict[str, Any]:
    """Set the Zalo bot webhook URL.

    Args:
        session: Shared aiohttp session.
        base_url: Base external URL for Home Assistant.
        webhook_id: Unique webhook identifier path.

    Returns:
        Zalo API JSON response as a dict.
    """
    url = f"https://bot-api.zapps.me/bot{TOKEN}/setWebhook"
    params = {
        "url": f"{base_url}/api/webhook/{webhook_id}",
        "secret_token": secrets.token_urlsafe(),  # A required parameter but ignored by Home Assistant.
    }
    async with session.post(url, json=params) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


async def _delete_webhook(session: aiohttp.ClientSession) -> dict[str, Any]:
    """Delete the Zalo bot webhook.

    Args:
        session: Shared aiohttp session.

    Returns:
        Zalo API JSON response as a dict.
    """
    url = f"https://bot-api.zapps.me/bot{TOKEN}/deleteWebhook"
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


async def _get_updates(
    session: aiohttp.ClientSession, timeout: int = 30
) -> dict[str, Any]:
    """Fetch updates with long polling.

    Args:
        session: Shared aiohttp session.
        timeout: Long-poll timeout in seconds.

    Returns:
        Zalo API JSON response as a dict.
    """
    url = f"https://bot-api.zapps.me/bot{TOKEN}/getUpdates"
    async with session.post(url, json={"timeout": timeout}) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


async def _get_me(session: aiohttp.ClientSession) -> dict[str, Any]:
    """Get basic information about the Zalo bot.

    Args:
        session: Shared aiohttp session.

    Returns:
        Zalo API JSON response as a dict.
    """
    url = f"https://bot-api.zapps.me/bot{TOKEN}/getMe"
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


async def _send_chat_action(
    session: aiohttp.ClientSession, chat_id: str, action: str = "typing"
) -> dict[str, Any]:
    """Send a chat action (e.g., typing) to a chat.

    Args:
        session: Shared aiohttp session.
        chat_id: Target chat identifier.
        action: Action name such as 'typing'.

    Returns:
        Zalo API JSON response as a dict.
    """
    url = f"https://bot-api.zapps.me/bot{TOKEN}/sendChatAction"
    params = {"chat_id": chat_id, "action": action}
    async with session.post(url, json=params) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


async def _copy_to_www(file_path: str) -> tuple[str, str]:
    """Copy a local media file to Home Assistant www/zalo and return its public URL and local destination path.

    Args:
        file_path: Input path that may start with local/ or /media/.

    Returns:
        Tuple of (public_url, dest_path).

    Raises:
        ValueError: When external URL is not configured.
    """
    normalized = _to_media_path(file_path)
    file_exists = await asyncio.to_thread(os.path.isfile, normalized)
    if not file_exists:
        raise FileNotFoundError(f"File not found: {normalized}")
    external = _external_url()
    if not external:
        raise ValueError("The external Home Assistant URL is not found or incorrect.")
    await _ensure_dir(WWW_DIRECTORY)

    name = f"{secrets.token_urlsafe(16)}-{Path(normalized).name}"
    dest_path = os.path.join(WWW_DIRECTORY, name)

    # Streaming copy
    async with (
        aiofiles.open(normalized, "rb") as src,
        aiofiles.open(dest_path, "wb") as dst,
    ):
        async for (
            chunk
        ) in src:  # aiofiles supports async iteration (default chunk size)
            await dst.write(chunk)

    public_url = f"{external}/local/zalo/{name}"
    return public_url, dest_path


async def _remove_file(path: str) -> None:
    """Remove a file path if exists."""
    try:
        await asyncio.to_thread(os.remove, path)
    except FileNotFoundError:
        return


async def _delayed_remove(path: str, delay_seconds: int = 30) -> None:
    """Wait for a delay and then remove a file.

    Args:
        path: Absolute filesystem path to remove.
        delay_seconds: Time to wait before removal.
    """
    await asyncio.sleep(delay_seconds)
    await _remove_file(path)


def _internal_url() -> str | None:
    """Return the internal Home Assistant URL, if available.

    Returns:
        Internal URL string or None when unavailable.
    """
    try:
        return network.get_url(hass, allow_external=False)
    except network.NoURLAvailableError:
        return None


def _external_url() -> str | None:
    """Return the external HTTPS Home Assistant URL, if available.

    Returns:
        External URL string or None when unavailable.
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


@time_trigger("shutdown")
async def _close_session() -> None:
    """Close the aiohttp session on shutdown."""
    global _session
    if _session and not _session.closed:
        await _session.close()
        _session = None


@time_trigger("cron(0 0 * * *)")
async def _daily_cleanup() -> None:
    """Run daily cleanup of old files."""
    await _cleanup_old_files(DIRECTORY, days=30)
    # Cleanup www folder more frequently or same duration? Assuming same.
    await _cleanup_old_files(
        WWW_DIRECTORY, days=1
    )  # Public files should be short-lived


@service(supports_response="only")
async def send_zalo_message(chat_id: str, message: str) -> dict[str, Any]:
    """
    yaml
    name: Send Zalo Message
    description: Send a plain text message to a Zalo chat via your bot.
    fields:
      chat_id:
        name: Chat ID
        description: Target chat ID.
        required: true
        selector:
          text:
      message:
        name: Message
        description: Message text (up to ~2000 chars).
        example: Hello from Home Assistant
        required: true
        selector:
          text:
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
    description: Download a file by direct URL and save it under Home Assistant media; returns a local path and file type.
    fields:
      url:
        name: URL
        description: Direct file URL (e.g., from a Zalo attachment).
        required: true
        selector:
          text:
    """
    if not url:
        return {"error": "Missing a required argument: url"}
    try:
        session = await _ensure_session()
        await _ensure_dir(DIRECTORY)

        file_path = await _download_file(session, url)
        if not file_path:
            return {"error": "Unable to download the file from Zalo."}

        mimetypes.add_type("text/plain", ".yaml")
        mime_type, _ = mimetypes.guess_file_type(file_path)
        file_path = _to_relative_path(file_path)
        response: dict[str, Any] = {"file_path": file_path, "mime_type": mime_type}
        support_file_types = (
            "image/",
            "video/",
            "audio/",
            "text/",
            "application/pdf",
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
    description: Retrieve current webhook configuration and status.
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
    description: Configure the HTTPS webhook endpoint for your Zalo bot.
    fields:
      webhook_id:
        name: Webhook ID
        description: Optional custom path suffix for /api/webhook; leave empty to auto-generate.
        selector:
          text:
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
    description: Remove the webhook configuration and stop webhook delivery.
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
    description: Fetch new messages via long polling (use when no webhook).
    fields:
      timeout:
        name: Timeout
        description: Server wait time before responding (30-60 seconds).
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
    description: Get basic bot profile and status.
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
    description: Show a 'typing' indicator in the chat.
    fields:
      chat_id:
        name: Chat ID
        description: ID of the conversation (user or group).
        required: true
        selector:
          text:
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


@service(supports_response="only")
async def send_zalo_photo(
    chat_id: str,
    file_path: str,
    caption: str | None = None,
) -> dict[str, Any]:
    """
    yaml
    name: Send Zalo Photo
    description: Send a local image by temporarily publishing it to /local/zalo and posting its URL to Zalo; the published file is deleted after a successful send.
    fields:
      chat_id:
        name: Chat ID
        description: ID of the conversation (user or group).
        required: true
        selector:
          text:
      file_path:
        name: File Path
        description: Local image path under /media or local/; the file is copied to /config/www/zalo temporarily.
        required: true
        selector:
          text:
      caption:
        name: Caption
        description: Optional text shown under the photo.
        selector:
          text:
    """
    if not all([chat_id, file_path]):
        return {"error": "Missing one or more required arguments: chat_id, file_path"}
    published_path = None
    try:
        session = await _ensure_session()
        public_url, published_path = await _copy_to_www(file_path)
        response = await _send_photo(session, chat_id, public_url, caption=caption)
        return response
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}
    finally:
        # Ensure deletion is scheduled even if an error occurred
        if published_path:
            task.create(_delayed_remove, published_path, 30)
