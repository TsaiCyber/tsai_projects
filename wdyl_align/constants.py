# coding: utf-8

import os

LANG_MAPPING = {
    'zh': '中文',
    'en': '英文',
    'ko': '韩语',
    'ja': '日语',
    'ru': '俄语',
    'es': '西班牙语',
    'tr': '土耳其语',
    'fr': '法语',
    'it': '意大利语',
    'hu': '匈牙利语',
    'pt': '葡萄牙语',
    'de': '德语',
    'ar': '阿拉伯语',
    'th': '泰语',}

INTERMEDIATE_FILES_BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "intermediate_files")
# UPLOAD_FOLDER = 'uploads'
ALLOWED_FILE_EXTENSIONS = {
    'docx',}

BASE_PROTOCOL = "http"
# BASE_PROTOCOL = "https"
BASE_HOST_DOMAIN = "117.50.220.141"
# BASE_HOST_DOMAIN = "106.75.46.58"
BASE_HOST_PORT = ":15000"
# BASE_HOST_PORT = ":18085"
TRANSLATION_API = f"{BASE_PROTOCOL}://{BASE_HOST_DOMAIN}{BASE_HOST_PORT}/translate_batch_v2"

# 长度短于 SENTENCE_IGNORE_LENGTH 的句子，不进行对齐
EN_SENTENCE_IGNORE_LENGTH = 10
ZH_SENTENCE_IGNORE_LENGTH = 2
