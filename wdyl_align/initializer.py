# coding: utf-8

"""
应用初始化模块
在应用启动时预加载所有必需的NLTK和spaCy模型，避免在请求处理过程中重复加载
"""

import os
from sentence_tokenizer.sentence_tokenizer import _ensure_nltk_punkt, _get_spacy_model
from wdyl_logger.wdyl_logger import logger
from constants import INTERMEDIATE_FILES_BASE_DIR


# Create uploads directory if it doesn't exist
os.makedirs(INTERMEDIATE_FILES_BASE_DIR, exist_ok=True)


def initialize_resources():
    """
    初始化所有必需的资源，包括NLTK数据包和spaCy模型
    """
    logger.info("🚀 开始初始化应用资源...")
    
    # 预加载NLTK punkt数据包
    _ensure_nltk_punkt()
    logger.info("✅ NLTK punkt数据包已准备就绪")
    
    # 预加载所需的spaCy模型
    # 目前只有英文模型，但可以轻松扩展以支持更多语言
    en_model = _get_spacy_model("en_core_web_sm")
    logger.info("✅ spaCy英文模型已准备就绪")
    
    logger.info("🎉 所有资源初始化完成！应用已准备好处理请求。")


if __name__ == "__main__":
    # 如果直接运行此脚本，则执行初始化
    initialize_resources()
