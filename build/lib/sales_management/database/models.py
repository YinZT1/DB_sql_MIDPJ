from database.db_connector import get_db_connection
from datetime import datetime
import sqlite3
'''
这里是实体的实现，所有的实体表都在这里。
每一个实体提供五个函数:建增删查改//

目前仅实现了增+查，部分实现了更新

'''
# 你需要完善以下类。
class Store:
    """门店模型"""
    @staticmethod
    def create(名称, 地点=None, 电话=None, 负责人=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Store (名称, 地点, 电话, 负责人) VALUES (?, ?, ?, ?)",
                (名称, 地点, 电话, 负责人)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_id(编号):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Store WHERE 编号=?", (编号,))
            return cursor.fetchone()

    @staticmethod
    def update(编号, 名称=None, 地点=None, 电话=None, 负责人=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            updates = []
            params = []
            if 名称:
                updates.append("名称=?")
                params.append(名称)
            if 地点:
                updates.append("地点=?")
                params.append(地点)
            if 电话:
                updates.append("电话=?")
                params.append(电话)
            if 负责人:
                updates.append("负责人=?")
                params.append(负责人)
            
            if updates:
                params.append(编号)
                cursor.execute(
                    f"UPDATE Store SET {','.join(updates)} WHERE 编号=?",
                    params
                )
                conn.commit()
                return cursor.rowcount
            return 0
        
    @staticmethod
    def delete(编号):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Store WHERE 编号=?", (编号,))
            conn.commit()
            return cursor.rowcount 
        return 0


class Product:
    """商品模型"""
    VALID_CATEGORIES = ('食品', '服装', '图书', '电子', '日用品')

    @staticmethod
    def create(条码, 名称, 销售价格, 类别, 计量单位=None):
        if 类别 not in Product.VALID_CATEGORIES:
            raise ValueError("无效的商品类别")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Product (条码, 名称, 计量单位, 销售价格, 类别) VALUES (?, ?, ?, ?, ?)",
                (条码, 名称, 计量单位, 销售价格, 类别)
            )
            conn.commit()
            return 条码

    @staticmethod
    def get_by_barcode(条码):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Product WHERE 条码=?", (条码,))
            return cursor.fetchone()
        
    @staticmethod
    def update(条码, 名称=None, 销售价格=None, 类别=None, 计量单位=None):
        updates = []
        params = []
        
        # 字段更新处理
        if 名称:
            updates.append("名称=?")
            params.append(名称)
        
        if 销售价格:
            if not isinstance(销售价格, (int, float)) or 销售价格 <= 0:
                raise ValueError("销售价格必须是正数")
            updates.append("销售价格=?")
            params.append(销售价格)
        
        if 类别:
            if 类别 not in Product.VALID_CATEGORIES:
                raise ValueError(f"无效类别，必须是以下之一：{Product.VALID_CATEGORIES}")
            updates.append("类别=?")
            params.append(类别)
        
        if 计量单位:
            updates.append("计量单位=?")
            params.append(计量单位)
        
        # 校验至少有一个有效更新
        if updates:
            params.append(条码)
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"UPDATE Store SET {','.join(updates)} WHERE 条码=?",
                    params
                )
                conn.commit()
                return cursor.rowcount
        return 0

    @staticmethod
    def delete(条码):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Product WHERE 条码=?", (条码,))
            conn.commit()
            return cursor.rowcount
        return 0

class Book:
    """图书模型(继承商品)"""
    @staticmethod
    def create(条码, 书名, 定价, 出版社=None, 书号=None, 作者=None, 出版时间=None, 版本号=None, 译者=None):
        # 先创建基础商品记录
        Product.create(条码, 书名, 定价, '图书', '本')
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO Book (条码, 书号, 书名, 作者, 定价, 出版社, 出版时间, 版本号, 译者)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (条码, 书号, 书名, 作者, 定价, 出版社, 出版时间, 版本号, 译者)
            )
            conn.commit()
            return 条码

    @staticmethod
    def get_by_barcode(条码):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.条码, p.名称 as 书名, b.书号, b.作者, b.定价, 
                       b.出版社, b.出版时间, b.版本号, b.译者
                FROM Product p
                JOIN Book b ON p.条码 = b.条码
                WHERE p.条码=?
            """, (条码,))
            return cursor.fetchone()
        
    @staticmethod
    def update(条码, 书号=None, 书名=None, 作者=None, 定价=None, 
            出版社=None, 出版时间=None, 版本号=None, 译者=None):
        updates = []
        params = []
        
        # 字段更新处理
        if 书号 is not None:
            updates.append("书号=?")
            params.append(书号)
        
        if 书名 is not None:
            updates.append("书名=?")
            params.append(书名)
        
        if 作者 is not None:
            updates.append("作者=?")
            params.append(作者)
        
        if 定价 is not None:
            if not isinstance(定价, (int, float)) or 定价 <= 0:
                raise ValueError("定价必须是正数")
            updates.append("定价=?")
            params.append(定价)
        
        if 出版社 is not None:
            updates.append("出版社=?")
            params.append(出版社)
        
        if 出版时间 is not None:
            updates.append("出版时间=?")
            params.append(出版时间)
        
        if 版本号 is not None:
            updates.append("版本号=?")
            params.append(版本号)
        
        if 译者 is not None:
            updates.append("译者=?")
            params.append(译者)
        
        # 校验至少有一个有效更新
        if updates:
            params.append(条码)
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"UPDATE Book SET {','.join(updates)} WHERE 条码=?",
                    params
                )
                conn.commit()
                return cursor.rowcount
        return 0
    
    @staticmethod
    def delete(条码):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # 开启事务
            conn.execute("BEGIN TRANSACTION")
            
            # 1. 先删除子表(Book)记录
            cursor.execute("DELETE FROM Book WHERE 条码=?", (条码,))
            book_deleted = cursor.rowcount
            
            # 2. 再删除主表(Product)记录
            cursor.execute("DELETE FROM Product WHERE 条码=?", (条码,))
            product_deleted = cursor.rowcount
            
            conn.commit()
            
            if book_deleted > 0 and product_deleted > 0:
                return book_deleted
            elif book_deleted == 0 and product_deleted == 0:
                return 0
            else:
                return -1
        return 0
    

class Supplier:
    """供货商模型"""
    @staticmethod
    def create(名称, 电话=None, email=None):
        if email and '@' not in email:
            raise ValueError("邮箱格式不正确")
            
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Supplier (名称, 电话, email) VALUES (?, ?, ?)",
                (名称, 电话, email)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def add_product_supplier(product_id, supplier_id):
        """添加商品-供货商关系"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Product_and_Supplier (product_id, supplier_id) VALUES (?, ?)",
                (product_id, supplier_id)
            )
            conn.commit()
            return True
        

class Member:
    """会员模型"""
    @staticmethod
    def create(姓名, 联系电话, email=None, 地址=None):
        # 先创建客户记录
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                # 检查是否已存在该电话的客户
                cursor.execute("SELECT 1 FROM Customer WHERE 联系电话=?", (联系电话,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO Customer (联系电话, 类型) VALUES (?, ?)",
                        (联系电话, '会员')
                    )
                
                # 创建会员记录
                cursor.execute(
                    """INSERT INTO Member (姓名, 联系电话, email, 地址)
                    VALUES (?, ?, ?, ?)""",
                    (姓名, 联系电话, email, 地址)
                )
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError as e:
                conn.rollback()
                raise ValueError("会员已存在或联系电话重复")

    @staticmethod
    def get_by_id(编号):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.编号, m.姓名, m.联系电话, m.email, m.地址, c.类型
                FROM Member m
                JOIN Customer c ON m.联系电话 = c.联系电话
                WHERE m.编号=?
            """, (编号,))
            return cursor.fetchone()

class Sale:
    """销售记录模型"""
    @staticmethod
    def create(单号, 关联门店, 关联商品, 数量, 金额, 日期=None, 关联客户=None):
        if not 日期:
            日期 = datetime.now().strftime("%Y-%m-%d")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """INSERT INTO Sale (单号, 日期, 数量, 金额, 关联门店, 关联商品, 关联客户)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (单号, 日期, 数量, 金额, 关联门店, 关联商品, 关联客户)
                )
                conn.commit()
                return 单号
            except sqlite3.Error as e:
                conn.rollback()
                raise ValueError("创建销售记录失败，请检查外键约束")

    @staticmethod
    def get_by_id(单号):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.单号, s.日期, s.数量, s.金额,
                       st.名称 as 门店名称, p.名称 as 商品名称,
                       CASE 
                           WHEN s.关联客户 IS NULL THEN '非会员'
                           ELSE m.姓名
                       END as 客户名称
                FROM Sale s
                JOIN Store st ON s.关联门店 = st.编号
                JOIN Product p ON s.关联商品 = p.条码
                LEFT JOIN Member m ON s.关联客户 = m.联系电话
                WHERE s.单号=?
            """, (单号,))
            return cursor.fetchone()

    @staticmethod
    def get_sales_by_store(门店编号, 开始日期=None, 结束日期=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT s.单号, s.日期, p.名称 as 商品名称, s.数量, s.金额
                FROM Sale s
                JOIN Product p ON s.关联商品 = p.条码
                WHERE s.关联门店=?
            """
            params = [门店编号]
            
            if 开始日期:
                query += " AND s.日期 >= ?"
                params.append(开始日期)
            if 结束日期:
                query += " AND s.日期 <= ?"
                params.append(结束日期)
            
            query += " ORDER BY s.日期 DESC"
            cursor.execute(query, params)
            return cursor.fetchall()