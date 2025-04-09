import sqlite3
import os
from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).parent

# 数据库配置
DATABASE_CONFIG = {
    'db_name': os.path.join(BASE_DIR, 'sales.db'),
    'timeout': 30,
    'detect_types': sqlite3.PARSE_DECLTYPES,
    'isolation_level': 'IMMEDIATE'  # SQLite事务隔离级别
}

# 日志配置
LOG_CONFIG = {
    'log_file': os.path.join(BASE_DIR, 'sales_management.log'),
    'log_level': 'INFO'
}