import asyncio
import mimetypes
import os
import secrets
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import aiohttp
from homeassistant.helpers import network

DIRECTORY = "/media/zalo"

_session: aiohttp.ClientSession | None = None


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


def _internal_url() -> str | None:
    """Return the internal Home Assistant URL, or None when it cannot be resolved."""
    try:
        return network.get_url(hass, allow_external=False)  # noqa: F821
    except network.NoURLAvailableError:
        return None


def _external_url() -> str | None:
    """Return the external HTTPS Home Assistant URL when configured and reachable."""
    try:
        return network.get_url(
            hass,  # noqa: F821
            allow_internal=False,
            allow_ip=False,
            require_ssl=True,
            require_standard_port=True,
        )
    except network.NoURLAvailableError:
        return None


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


@pyscript_compile  # noqa: F821
def _open_file(path: str, mode: str):
    """Open a file safely using native Python."""
    return open(path, mode)


@pyscript_compile  # noqa: F821
def _cleanup_disk_sync(directory: str, cutoff: float) -> None:
    """Native Python function to perform disk cleanup safely."""
    path = Path(directory)
    if not path.exists():
        return

    for entry in path.iterdir():
        try:
            if entry.is_file():
                # Extracting variable for clarity
                file_mtime = entry.stat().st_mtime
                if file_mtime < cutoff:
                    entry.unlink()
        except OSError:
            # Silently skip files that are locked or inaccessible
            pass


async def _cleanup_old_files(directory: str, days: int = 30) -> None:
    """Delete files in the directory older than the specified number of days."""
    now = time.time()
    cutoff = now - (days * 86400)
    await asyncio.to_thread(_cleanup_disk_sync, directory, cutoff)


async def _download_file(
    session: aiohttp.ClientSession, url: str
) -> tuple[str, None] | tuple[None, str]:
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

            parsed_url = urlparse(url)
            original_name = Path(parsed_url.path).name
            if not Path(original_name).suffix and ext:
                original_name += ext

            base, extension = os.path.splitext(original_name)
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            file_name = f"{base}_{timestamp}_{secrets.token_hex(4)}{extension}"

            file_path = os.path.join(DIRECTORY, file_name)

            f = await asyncio.to_thread(_open_file, file_path, "wb")
            try:
                async for chunk in resp.content.iter_chunked(65536):
                    if chunk:
                        await asyncio.to_thread(f.write, chunk)
                await asyncio.to_thread(f.flush)
                await asyncio.to_thread(os.fsync, f.fileno())
            finally:
                await asyncio.to_thread(f.close)

            return file_path, None
    except Exception as error:
        return None, f"An unexpected error occurred during download: {error}"


@time_trigger("shutdown")  # noqa: F821
async def _close_session() -> None:
    """Close the aiohttp session on shutdown."""
    global _session
    if _session and not _session.closed:
        await _session.close()
        _session = None


@time_trigger("cron(0 0 * * *)")  # noqa: F821
async def _daily_cleanup() -> None:
    """Run daily cleanup of old files."""
    await _cleanup_old_files(DIRECTORY, days=30)


@service(supports_response="only")  # noqa: F821
async def get_zalo_file_custom_bot(url: str) -> dict[str, Any]:
    """
    yaml
    name: Get Zalo File (Custom Bot)
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

        file_path, error = await _download_file(session, url)
        if not file_path:
            return {"error": f"Unable to download the file from Zalo. {error}"}

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


@service(supports_response="only")  # noqa: F821
async def generate_webhook_id() -> dict[str, Any]:
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
