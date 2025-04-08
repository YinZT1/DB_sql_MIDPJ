from database.models import Product, Book, Supplier
from utils.logger import setup_logger
import sqlite3
logger = setup_logger()

class ProductService:
    """商品服务"""
    
    @staticmethod
    def add_product(条码, 名称, 销售价格, 类别, 计量单位=None):
        try:
            if float(销售价格) <= 0:
                raise ValueError("销售价格必须大于0")
                
            product_id = Product.create(条码, 名称, 销售价格, 类别, 计量单位)
            logger.info(f"成功添加商品: {名称}, 条码: {条码}")
            return product_id
        except ValueError as e:
            logger.error(f"添加商品验证失败: {e}")
            raise
        except sqlite3.Error as e:
            logger.error(f"添加商品失败: {e}")
            raise ValueError("添加商品失败，请检查条码是否重复")
    
    @staticmethod
    def add_book(条码, 书名, 定价, **kwargs):
        try:
            if float(定价) <= 0:
                raise ValueError("定价必须大于0")
                
            book_id = Book.create(条码, 书名, 定价, **kwargs)
            logger.info(f"成功添加图书: {书名}, 条码: {条码}")
            return book_id
        except ValueError as e:
            logger.error(f"添加图书验证失败: {e}")
            raise
        except sqlite3.Error as e:
            logger.error(f"添加图书失败: {e}")
            raise ValueError("添加图书失败，请检查数据是否正确")

class SupplierService:
    """供货商服务"""
    
    @staticmethod
    def add_supplier(名称, 电话=None, email=None):
        try:
            supplier_id = Supplier.create(名称, 电话, email)
            logger.info(f"成功添加供货商: {名称}, ID: {supplier_id}")
            return supplier_id
        except ValueError as e:
            logger.error(f"添加供货商验证失败: {e}")
            raise
        except sqlite3.Error as e:
            logger.error(f"添加供货商失败: {e}")
            raise ValueError("添加供货商失败")
    
    @staticmethod
    def link_product_supplier(product_id, supplier_id):
        try:
            success = Supplier.add_product_supplier(product_id, supplier_id)
            logger.info(f"成功关联商品{product_id}与供货商{supplier_id}")
            return success
        except sqlite3.Error as e:
            logger.error(f"关联商品供货商失败: {e}")
            raise ValueError("关联失败，请检查ID是否存在")