import logging
from pathlib import Path
from sales_management.config import LOG_CONFIG

'''
default:
- name: logger
- LOG_CONFIG: LOG_CONFIG = {

    'log_file': os.path.join(BASE_DIR, 'sales_management.log'),
    'log_level': 'INFO'

}
'''

def setup_logger(name=__name__):
    """配置并返回一个日志记录器"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # 避免重复添加handler
        logger.setLevel(LOG_CONFIG['log_level'])
        
        # 创建文件handler
        file_handler = logging.FileHandler(
            LOG_CONFIG['log_file'],
            encoding='utf-8'
        )
        file_handler.setLevel(LOG_CONFIG['log_level'])
        
        # 创建控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_CONFIG['log_level'])
        
        # 创建formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加handler
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger