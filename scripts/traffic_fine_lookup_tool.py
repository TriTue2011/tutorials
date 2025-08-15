import asyncio
import json
import re
import ssl
from datetime import timedelta
from io import BytesIO

import aiohttp
import google.api_core.exceptions
import google.genai
import redis.asyncio as redis
from PIL import Image
from PIL import ImageOps
from bs4 import BeautifulSoup
from bs4.element import AttributeValueList

TTL = 24
RETRY_LIMIT = 3
GET_URL = "https://www.csgt.vn/"
POST_URL = "https://www.csgt.vn/?mod=contact&task=tracuu_post&ajax"
CAPTCHA_URL = "https://www.csgt.vn/lib/captcha/captcha.class.php"
GET_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "www.csgt.vn",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}
POST_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1",
    "Host": "www.csgt.vn",
    "Origin": "https://www.csgt.vn",
    "Pragma": "no-cache",
    "Referer": "https://www.csgt.vn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_API_KEY = pyscript.config.get("gemini_api_key")
REDIS_HOST = pyscript.config.get("redis_host")
REDIS_PORT = pyscript.config.get("redis_port")

if not GEMINI_API_KEY:
    raise ValueError("You need to configure your Gemini API key")

if not all([REDIS_HOST, REDIS_PORT]):
    raise ValueError("You need to configure your Redis host and port")

client = google.genai.Client(api_key=GEMINI_API_KEY)

cached = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@pyscript_compile
def extract_violations_from_html(content: str, url: str) -> dict:
    soup = BeautifulSoup(content, "html.parser")
    violations = []
    body_print = soup.find("div", id="bodyPrint123")

    if not body_print:
        return {
            "status": "failure",
            "url": url,
            "message": "Không tìm thấy dữ liệu vi phạm",
            "detail": "",
        }

    sections = body_print.find_all(recursive=False)
    current_violation = None
    for element in sections:
        if "form-group" in element.get("class", AttributeValueList()):
            if current_violation is None:
                current_violation = {
                    "Biển kiểm soát": "",
                    "Màu biển": "",
                    "Loại phương tiện": "",
                    "Thời gian vi phạm": "",
                    "Địa điểm vi phạm": "",
                    "Hành vi vi phạm": "",
                    "Trạng thái": "",
                    "Đơn vị phát hiện vi phạm": "",
                    "Nơi giải quyết vụ việc": [],
                }

            label = element.find("label", class_="control-label")
            value = element.find("div", class_="col-md-9")
            if label and value:
                key = label.get_text(strip=True).replace(":", "")
                val = value.get_text(strip=True)
                if key in current_violation:
                    if key != "Nơi giải quyết vụ việc":
                        current_violation[key] = val

            text = element.get_text(strip=True)
            if text and re.match(r"[1-9]\. |Địa chỉ:|Số điện thoại liên hệ:", text):
                current_violation["Nơi giải quyết vụ việc"].append(text)

        elif element.name == "hr":
            if current_violation:
                violations.append(current_violation)
                current_violation = None

    if current_violation:
        violations.append(current_violation)

    if not violations:
        return {
            "status": "success",
            "url": url,
            "message": "Không có vi phạm giao thông",
            "detail": "",
        }

    return {
        "status": "success",
        "url": url,
        "message": f"Có {len(violations)} vi phạm giao thông",
        "detail": violations,
    }


@pyscript_compile
async def get_captcha(
    ss: aiohttp.ClientSession, url: str
) -> tuple[BytesIO, None] | tuple[None, str]:
    try:
        async with ss.get(url, timeout=30) as response:
            response.raise_for_status()
            content = await response.read()
            return BytesIO(content), None
    except asyncio.TimeoutError as error:
        return None, f"TimeoutError during retrieve CAPTCHA image: {error}"
    except aiohttp.ClientError as error:
        return None, f"ClientError during retrieve CAPTCHA image: {error}"
    except Exception as error:
        return None, f"An unexpected error during retrieve CAPTCHA image: {error}"


@pyscript_compile
def process_captcha(
    image: str | BytesIO, threshold: int = 180, factor: int = 8, padding: int = 35
) -> Image.Image:
    img = Image.open(image)
    img = img.convert("L")
    img = ImageOps.autocontrast(img, cutoff=2)
    table = [0] * threshold + [255] * (256 - threshold)
    img = img.point(table)
    img = img.resize(
        (img.width * factor, img.height * factor), resample=Image.Resampling.BOX
    )
    img = img.convert("RGBA")
    for x in range(img.width):
        for y in range(img.height):
            (r, g, b, a) = img.getpixel((x, y))
            if (r, g, b) == (255, 255, 255):
                img.putpixel((x, y), (r, g, b, 0))
    bbox = img.getbbox()
    if bbox:
        (left, upper, right, lower) = bbox
        left = max(0, left - padding)
        upper = max(0, upper - padding)
        right = min(img.width, right + padding)
        lower = min(img.height, lower + padding)
        img = img.crop((left, upper, right, lower))
    img = img.convert("L")
    return img


@pyscript_compile
async def solve_captcha(
    image: Image.Image, retry_count: int = 1
) -> tuple[str, None] | tuple[None, str]:
    prompt = "Extract exactly six consecutive lowercase letters (a-z) and digits (0-9) from this image, no spaces, and output only these characters."
    loop = asyncio.get_event_loop()
    try:
        response = await loop.run_in_executor(
            None,
            lambda: client.models.generate_content(
                model=GEMINI_MODEL, contents=[prompt, image]
            ),
        )
        if response.candidates and response.candidates[0].content.parts:
            generated_text = response.candidates[0].content.parts[0].text.strip()
            return generated_text, None
        else:
            reason = (
                response.candidates[0].finish_reason
                if response.candidates
                else "Unknown"
            )
            return None, f"CAPTCHA solving was not successful for reason: {reason}"
    except google.api_core.exceptions.ResourceExhausted as error:
        if retry_count < RETRY_LIMIT:
            print(
                f"Quota exceeded. Retrying in 30 seconds... (Attempt {retry_count}/{RETRY_LIMIT}): {error}"
            )
            await asyncio.sleep(30)
            return await solve_captcha(image, retry_count + 1)
        else:
            return (
                None,
                f"Quota exhausted and retry limit ({retry_count}/{RETRY_LIMIT}) reached: {error}",
            )
    except AttributeError as error:
        return (
            None,
            f"Possibly incorrect field in the response. Check for proper API handling: {error}",
        )
    except Exception as error:
        return None, f"An unexpected error occurred during CAPTCHA solving: {error}"


@pyscript_compile
async def check_license_plate(
    license_plate: str, vehicle_type: int, retry_count: int = 1
) -> dict:
    ssl_context = ssl.create_default_context()
    ssl_context.set_ciphers(
        "@SECLEVEL=0:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA256:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA"
    )
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as ss:
        try:
            async with ss.get(GET_URL, headers=GET_HEADERS, timeout=30) as response_1st:
                response_1st.raise_for_status()
                image, error = await get_captcha(ss, CAPTCHA_URL)

                if not image:
                    return {"error": f"Unable to retrieve CAPTCHA image: {error}"}

                image_filtered = process_captcha(image)
                captcha, error = await solve_captcha(image_filtered)

                if not captcha:
                    return {"error": f"CAPTCHA solving was not successful: {error}"}

                captcha = re.sub(r"[^a-zA-Z0-9]", "", captcha).lower()

                data = f"BienKS={license_plate}&Xe={vehicle_type}&captcha={captcha}&ipClient=9.9.9.91&cUrl=1"

                async with ss.post(
                    url=POST_URL, headers=POST_HEADERS, data=data, timeout=30
                ) as response_2nd:
                    response_2nd.raise_for_status()
                    response_2nd_json = await response_2nd.json(
                        content_type="text/html"
                    )
                    url = response_2nd_json.get("href")

                    if not url:
                        if retry_count < RETRY_LIMIT:
                            print(
                                f"Retrying in 15 seconds... (Attempt {retry_count}/{RETRY_LIMIT})"
                            )
                            await asyncio.sleep(15)
                            return await check_license_plate(
                                license_plate, vehicle_type, retry_count + 1
                            )
                        else:
                            return {
                                "error": f"Retry limit ({retry_count}/{RETRY_LIMIT}) reached"
                            }

                    async with ss.get(url=url, timeout=30) as response_3rd:
                        response_3rd.raise_for_status()
                        text_content = await response_3rd.text()
                        response = extract_violations_from_html(text_content, url)

                        if response and response.get("status") == "success":
                            await cached.set(
                                f"{license_plate}-{vehicle_type}", json.dumps(response)
                            )
                            await cached.expire(
                                f"{license_plate}-{vehicle_type}", timedelta(hours=TTL)
                            )
                        return response

        except Exception as error:
            if retry_count < RETRY_LIMIT:
                print(
                    f"Retrying in 15 seconds... (Attempt {retry_count}/{RETRY_LIMIT}): {error}"
                )
                await asyncio.sleep(15)
                return await check_license_plate(
                    license_plate, vehicle_type, retry_count + 1
                )
            else:
                return {
                    "error": f"Retry limit ({retry_count}/{RETRY_LIMIT}) reached: {error}"
                }


@service(supports_response="only")
async def traffic_fine_lookup_tool(
    license_plate: str, vehicle_type: int, bypass_caching: bool = False
) -> dict:
    """
    yaml
    name: Traffic Fine Lookup Tool
    description: Tool to check Vietnam traffic fines.
    fields:
      license_plate:
        name: License Plate
        description: The license plate number of vehicle.
        example: 29A99999
        required: true
        selector:
          text: {}
      vehicle_type:
        name: Vehicle Type
        description: The type of vehicle.
        example: '"1"'
        required: true
        selector:
          select:
            options:
              - label: Ô tô
                value: "1"
              - label: Xe máy
                value: "2"
              - label: Xe đạp điện
                value: "3"
        default: "1"
      bypass_caching:
        name: Bypass Caching
        description: Bypass the cache to retrieve the latest data from csgt.vn.
        example: false
        selector:
          boolean: {}
    """
    try:
        license_plate = str(license_plate).upper()
        vehicle_type = int(vehicle_type)

        if vehicle_type == 1:
            pattern = r"^\d{2}[A-Z]{1,2}\d{4,5}$"
        else:
            pattern = r"^\d{2}[A-Z1-9]{2}\d{4,5}$"
        if not (license_plate and re.match(pattern, license_plate)):
            return {"error": "The license plate number is invalid"}

        if vehicle_type not in [1, 2, 3]:
            return {"error": "The type of vehicle is invalid"}

        if bool(bypass_caching):
            await cached.delete(f"{license_plate}-{vehicle_type}")
            return await check_license_plate(license_plate, vehicle_type)

        response = await cached.get(f"{license_plate}-{vehicle_type}")
        if response:
            return json.loads(response)
        return await check_license_plate(license_plate, vehicle_type)
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}
