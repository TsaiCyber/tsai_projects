import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json

from wdyl_logger.wdyl_logger import logger


# 定义重试策略
retry = Retry(
    total=3,  # 总重试次数（含首次共4次）
    backoff_factor=1,  # 指数退避：0s,1s,2s,4s...
    status_forcelist=[500,502,503,504,429],  # 这些状态码触发重试
    allowed_methods=["POST"],  # 允许重试 POST（谨慎！）
)


BASE_PROTOCOL = "http"
# BASE_HOST_DOMAIN = "117.50.220.141"
BASE_HOST_DOMAIN = "106.75.46.58"
# BASE_HOST_PORT = ":15000"
BASE_HOST_PORT = ":18085"
TRANSLATION_API = f"{BASE_PROTOCOL}://{BASE_HOST_DOMAIN}{BASE_HOST_PORT}/translate_batch_v2"


def get_translated_result(request_url:str=TRANSLATION_API,
                          content:str='',
                          language_direction:tuple=("en", "zh")):
    headers = {"Content-Type": "application/json"}

    body_data = {"domain": "medical",
                 "qs": [content],
                 "source": language_direction[0],
                 "target": language_direction[1],}

    params = {"instance_id": "xxx",
              "application_id": "xxx", }

    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        resp = session.post(request_url,
                            headers=headers,
                            json=body_data,
                            params=params,
                            timeout=30)

        if resp.status_code == 200:
            translation_result = resp.json()['translation'][0]
            logger.debug(f"翻译结果: {translation_result}")
            return translation_result
        else:
            logger.error(f"请求失败! 状态码: {resp.status_code}")
            logger.error(f"错误信息: {resp.text}")
            return ""
    except requests.exceptions.RequestException as e:
        logger.error(f"请求异常: {e}")
        return ""
