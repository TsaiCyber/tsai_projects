import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json

from constants import TRANSLATION_API
from wdyl_logger.wdyl_logger import logger


# 定义重试策略
retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504, 429],
    allowed_methods=["POST"],)


def get_translated_result(request_url:str=TRANSLATION_API,
                          content:str='',
                          language_direction:tuple=("en", "zh")):
    try:
        if not content:
            raise ValueError("content is empty")

        headers = {"Content-Type": "application/json"}

        body_data = {"domain": "medical",
                     "qs": [content],
                     "source": language_direction[0],
                     "target": language_direction[1],}

        params = {"instance_id": "xxx",
                  "application_id": "xxx", }

        adapter = HTTPAdapter(max_retries=retry)
        session = requests.Session()
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        resp = session.post(request_url,
                            headers=headers,
                            json=body_data,
                            params=params,
                            timeout=30)

        if resp.status_code == 200:
            translation_result = resp.json()['translation'][0]
            # logger.debug(f"翻译结果: {translation_result}")
            return translation_result
        else:
            logger.error(f"请求失败! 状态码: {resp.status_code}")
            logger.error(f"错误信息: {resp.text}")
            return ""
    except requests.exceptions.RequestException as e:
        logger.error(f"请求异常: {e}")
        return ""


def get_translated_content_list(content_list:list,
                                language_direction:tuple=("en", "zh")):
    """
    批量翻译内容列表
    """
    translated_content_list = []
    for content in content_list:
        translated_content = get_translated_result(content=content,
                                                   language_direction=language_direction)
        # logger.info(translated_content)
        translated_content_list.append(translated_content)
    return translated_content_list
