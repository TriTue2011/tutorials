import asyncio
import mimetypes
import os
from pathlib import Path
from typing import Any

import aiofiles
import aiohttp

DIRECTORY = "/media/zalo"

_session: aiohttp.ClientSession | None = None


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


@service(supports_response="only")
async def get_zalo_file_custom_bot(url: str) -> dict[str, Any]:
    """
    yaml
    name: Get Zalo File
    description: Tool for retrieving and downloading media files directly from Zalo messages or groups.
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

        mimetypes.add_type("text/plain", ".yaml")
        mime_type, encoding = mimetypes.guess_file_type(file_path)
        file_path = file_path.replace(
            "/media/", "local/"
        )  # Modify the media source to use a relative URI
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
