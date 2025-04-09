import sqlite3
from pathlib import Path
from .db_connector import get_db_connection
from sales_management.config import DATABASE_CONFIG

def init_db():
    """初始化数据库，创建所有表结构"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 启用外键约束(SQLite默认关闭)
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # 检查是否已初始化
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Store'")
        
        if not cursor.fetchone():
            # 执行schema.sql中的SQL语句
            schema_file = Path(__file__).parent / 'schema.sql'
            with open(schema_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            cursor.executescript(sql_script)
            conn.commit()
            print("数据库初始化完成")

def reset_db():
    """重置数据库(开发用)"""
    db_path = DATABASE_CONFIG['db_name']
    if Path(db_path).exists():
        Path(db_path).unlink()
    init_db()