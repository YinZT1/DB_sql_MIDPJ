import sqlite3
from contextlib import contextmanager
from sales_management.config import DATABASE_CONFIG

@contextmanager
def get_db_connection():
    """
    获取数据库连接的上下文管理器
    使用示例：
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM table")
    """
    conn = None
    try:
        conn = sqlite3.connect(
            DATABASE_CONFIG['db_name'],
            timeout=DATABASE_CONFIG['timeout'],
            detect_types=DATABASE_CONFIG['detect_types'],
            isolation_level=DATABASE_CONFIG['isolation_level']
        )
        conn.row_factory = sqlite3.Row  # 使返回结果为字典式访问
        yield conn
    except sqlite3.Error as e:
        print(f"数据库连接错误: {e}")
        raise
    finally:
        if conn:
            conn.close()

@contextmanager
def get_db_cursor():
    """获取数据库游标的上下文管理器"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except:
            conn.rollback()
            raise