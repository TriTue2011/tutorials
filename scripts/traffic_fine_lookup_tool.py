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
from PIL.ImageFile import ImageFile
from PIL.ImageFilter import EDGE_ENHANCE
from bs4 import BeautifulSoup
from bs4.element import AttributeValueList

TTL = 3
RETRY_LIMIT = 3
GET_URL = 'https://www.csgt.vn/'
POST_URL = 'https://www.csgt.vn/?mod=contact&task=tracuu_post&ajax'
CAPTCHA_URL = 'https://www.csgt.vn/lib/captcha/captcha.class.php'
GET_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'www.csgt.vn',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}
POST_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Host': 'www.csgt.vn',
    'Origin': 'https://www.csgt.vn',
    'Pragma': 'no-cache',
    'Referer': 'https://www.csgt.vn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}
GEMINI_API_KEY = pyscript.config.get('gemini_api_key')
GEMINI_MODEL = 'gemini-2.5-flash'

if not GEMINI_API_KEY:
    raise ValueError("You need to configure your Gemini API key")

client = google.genai.Client(api_key=GEMINI_API_KEY)

cached = redis.Redis(host='localhost', port=6379, decode_responses=True)


@pyscript_compile
def extract_violations_from_html(content: str, url: str) -> dict:
    soup = BeautifulSoup(content, 'html.parser')
    violations = []
    body_print = soup.find('div', id='bodyPrint123')

    if not body_print:
        return dict(status='failure', url=url, message='Không tìm thấy dữ liệu vi phạm', detail='')

    sections = body_print.find_all(recursive=False)
    current_violation = None
    for element in sections:
        if 'form-group' in element.get('class', AttributeValueList()):
            if current_violation is None:
                current_violation = {
                    'Biển kiểm soát': '',
                    'Màu biển': '',
                    'Loại phương tiện': '',
                    'Thời gian vi phạm': '',
                    'Địa điểm vi phạm': '',
                    'Hành vi vi phạm': '',
                    'Trạng thái': '',
                    'Đơn vị phát hiện vi phạm': '',
                    'Nơi giải quyết vụ việc': []
                }

            label = element.find('label', class_='control-label')
            value = element.find('div', class_='col-md-9')
            if label and value:
                key = label.get_text(strip=True).replace(':', '')
                val = value.get_text(strip=True)
                if key in current_violation:
                    if key != 'Nơi giải quyết vụ việc':
                        current_violation[key] = val

            text = element.get_text(strip=True)
            if text and re.match(r'[1-9]\. |Địa chỉ:|Số điện thoại liên hệ:', text):
                current_violation['Nơi giải quyết vụ việc'].append(text)

        elif element.name == 'hr':
            if current_violation:
                violations.append(current_violation)
                current_violation = None

    if current_violation:
        violations.append(current_violation)

    if not violations:
        return dict(status='success', url=url, message='Không có vi phạm giao thông', detail='')

    return dict(status='success', url=url, message=f'Có {len(violations)} vi phạm giao thông', detail=violations)


@pyscript_compile
async def get_captcha(ss: aiohttp.ClientSession, url: str) -> tuple[BytesIO, None] | tuple[None, str]:
    try:
        async with ss.get(url, timeout=30) as response:
            response.raise_for_status()
            content = await response.read()
            return BytesIO(content), None
    except asyncio.TimeoutError as error:
        return None, f'TimeoutError during retrieve CAPTCHA image. Detail: {error}'
    except aiohttp.ClientError as error:
        return None, f'ClientError during retrieve CAPTCHA image. Detail: {error}'
    except Exception as error:
        return None, f'An unexpected error during retrieve CAPTCHA image. Detail: {error}'


@pyscript_compile
def process_captcha(image: str | BytesIO) -> ImageFile:
    image_pil = Image.open(image)
    threshold_value = 64
    image_threshold = image_pil.point(lambda p: p > threshold_value and 255)
    image_painted = image_threshold.filter(EDGE_ENHANCE)
    return image_painted


@pyscript_compile
async def solve_captcha(image: ImageFile, retry_count: int = 1) -> tuple[str, None] | tuple[None, str]:
    prompt = 'Extract the text from this image.'
    loop = asyncio.get_event_loop()
    try:
        response = await loop.run_in_executor(
            None,
            lambda: client.models.generate_content(model=GEMINI_MODEL, contents=[prompt, image])
        )
        if response.candidates and response.candidates[0].content.parts:
            generated_text = response.candidates[0].content.parts[0].text.strip()
            return generated_text, None
        else:
            reason = response.candidates[0].finish_reason if response.candidates else 'Unknown'
            return None, f'CAPTCHA solving was not successful for reason: {reason}'
    except google.api_core.exceptions.ResourceExhausted as error:
        if retry_count < RETRY_LIMIT:
            print(f'Quota exceeded. Retrying in 30 seconds... (Attempt {retry_count}/{RETRY_LIMIT}). Detail: {error}')
            await asyncio.sleep(30)
            return await solve_captcha(image, retry_count + 1)
        else:
            return None, f'Quota exhausted and retry limit ({retry_count}/{RETRY_LIMIT}) reached. Detail: {error}'
    except AttributeError as error:
        return None, f'Possibly incorrect field in the response. Check for proper API handling. Detail: {error}'
    except Exception as error:
        return None, f'An unexpected error occurred during CAPTCHA solving. Detail: {error}'


@pyscript_compile
async def check_license_plate(license_plate: str, vehicle_type: int, retry_count: int = 1) -> dict:
    ssl_context = ssl.create_default_context()
    ssl_context.set_ciphers(
        '@SECLEVEL=0:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA256:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA')
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as ss:
        try:
            async with ss.get(GET_URL, headers=GET_HEADERS, timeout=30) as response_1st:
                response_1st.raise_for_status()
                image, error = await get_captcha(ss, CAPTCHA_URL)

                if not image:
                    return dict(error='Unable to retrieve CAPTCHA image', detail=error)

                image_filtered = process_captcha(image)
                captcha, error = await solve_captcha(image_filtered)

                if not captcha:
                    return dict(error='CAPTCHA solving was not successful', detail=error)

                captcha = re.sub(r'[^a-zA-Z0-9]', '', captcha).lower()

                data = f'BienKS={license_plate}&Xe={vehicle_type}&captcha={captcha}&ipClient=9.9.9.91&cUrl=1'

                async with ss.post(url=POST_URL, headers=POST_HEADERS, data=data, timeout=30) as response_2nd:
                    response_2nd.raise_for_status()
                    response_2nd_json = await response_2nd.json(content_type='text/html')
                    url = response_2nd_json.get('href')

                    if not url:
                        if retry_count < RETRY_LIMIT:
                            print(f'Retrying in 15 seconds... (Attempt {retry_count}/{RETRY_LIMIT})')
                            await asyncio.sleep(15)
                            return await check_license_plate(license_plate, vehicle_type, retry_count + 1)
                        else:
                            return dict(error=f'Retry limit ({retry_count}/{RETRY_LIMIT}) reached. Exiting...',
                                        detail='')

                    async with ss.get(url=url, timeout=30) as response_3rd:
                        response_3rd.raise_for_status()
                        text_content = await response_3rd.text()
                        response = extract_violations_from_html(text_content, url)

                        if response and response.get('status') == 'success':
                            await cached.set(f'{license_plate}-{vehicle_type}', json.dumps(response))
                            await cached.expire(f'{license_plate}-{vehicle_type}', timedelta(hours=TTL))
                        return response

        except Exception as error:
            if retry_count < RETRY_LIMIT:
                print(f'Retrying in 15 seconds... (Attempt {retry_count}/{RETRY_LIMIT}). Detail: {error}')
                await asyncio.sleep(15)
                return await check_license_plate(license_plate, vehicle_type, retry_count + 1)
            else:
                return dict(error=f'Retry limit ({retry_count}/{RETRY_LIMIT}) reached. Exiting...', detail=error)


@service(supports_response='only')
async def traffic_fine_lookup_tool(license_plate: str, vehicle_type: int, bypass_caching: bool = False) -> dict:
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
            pattern = r'^\d{2}[A-Z]{1,2}\d{5}$'
        else:
            pattern = r'^\d{2}[A-Z1-9]{2}\d{5}$'
        if not (license_plate and re.match(pattern, license_plate)):
            return dict(error='The license plate number is invalid', detail='')

        if vehicle_type not in [1, 2, 3]:
            return dict(error='The type of vehicle is invalid', detail='')

        if bool(bypass_caching):
            await cached.delete(f'{license_plate}-{vehicle_type}')
            return await check_license_plate(license_plate, vehicle_type)

        response = await cached.get(f'{license_plate}-{vehicle_type}')
        if response:
            return json.loads(response)
        return await check_license_plate(license_plate, vehicle_type)
    except Exception as error:
        return dict(error=f'An unexpected error occurred during processing', detail=error)
