import sys
import logging

# 1. 获取以当前模块名命名的日志记录器，便于区分日志来源
logger = logging.getLogger(__name__)

# 2. 设置日志级别为 DEBUG
logger.setLevel(logging.DEBUG)

# 3. 检查是否已经存在处理器（防止被其他模块引用时重复添加处理器）
if not logger.hasHandlers():
    # 4. 创建一个 StreamHandler，指定输出到标准输出（终端）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # 5. 设置日志的打印格式（包含时间、级别、模块名和具体信息）
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # 6. 将处理器添加到日志记录器中
    logger.addHandler(console_handler)

# 测试代码（只有直接运行该模块时才会执行）
if __name__ == '__main__':
    logger.debug("这是一条调试(D)信息")
    logger.info("这是一条常规(I)信息")
    logger.warning("这是一条警告(W)信息")
    logger.error("这是一条错误(E)信息")