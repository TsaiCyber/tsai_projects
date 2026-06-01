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
ALLOWED_EXTENSIONS = {'docx',}
