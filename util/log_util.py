import colorlog
import logging
import os
from datetime import datetime

def setup_logger(name='app', level=logging.INFO):
    """
    设置日志记录器的配置
    :param name: 日志记录器的名称
    :param level: 日志级别
    :return: 配置好的日志记录器
    """
    # 获取日志文件
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_folder_path = os.path.join("../logs", current_date)
    os.makedirs(log_folder_path, exist_ok=True)
    log_file_path = os.path.join(log_folder_path, f"{name}.log")

    # 创建控制台日志处理器
    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    ))

    # 创建文件日志处理器
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 创建日志记录器
    logger = colorlog.getLogger(name)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(level)
    return logger

# 创建日志记录器
default_logger = setup_logger()