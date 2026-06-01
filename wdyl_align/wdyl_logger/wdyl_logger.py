# coding: utf-8

import sys
import logging


logger = logging.getLogger('Files Alignment')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout)


logger.setLevel(logging.DEBUG)


if not logger.hasHandlers():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


# 测试代码（只有直接运行该模块时才会执行）
if __name__ == '__main__':
    logger.debug("这是一条调试(D)信息")
    logger.info("这是一条常规(I)信息")
    logger.warning("这是一条警告(W)信息")
    logger.error("这是一条错误(E)信息")