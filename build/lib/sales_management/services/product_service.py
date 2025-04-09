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
            logger.info(f"成功添加商品-{类别}: {名称}, 条码: {条码}")
            return product_id
        except ValueError as e:
            logger.error(f"添加商品-{类别}验证失败: {e}")
            raise
        except sqlite3.Error as e:
            logger.error(f"添加商品-{类别}失败: {e}")
            raise ValueError(f"添加商品-{类别}失败，请检查条码是否重复")
    
    @staticmethod
    def get_product_info(条码):
        pruduct = Product.get_by_barcode(条码)
        if not pruduct:
            logger.warning(f"未找到商品: {条码}")
            return None
        
        logger.info(f"查询商品信息: {条码}")
        return {
            '条码': pruduct['条码'],
            '名称': pruduct['名称'],
            '销售价格': pruduct['销售价格'],
            '类别': pruduct['类别'],
            '计量单位': pruduct['计量单位']
        }
    

    @staticmethod
    def update_product_info(条码, **kwargs):
        try:
            product = ProductService.get_product_info(条码)
            affected = Product.update(条码, **kwargs)
            if affected > 0:
                logger.info(f"成功更新商品-{product['类别']}: {条码}")
                return True
            logger.warning(f"未更新商品-{product['类别']}: {条码}, 可能未提供有效更改")
            return False
        except sqlite3.Error as e:
            logger.error(f"更新商品-{product['类别']}失败: {e}")
            raise ValueError(f"更新商品-{product['类别']}信息失败")
        
    @staticmethod
    def delete_pruduct(条码):
        try:
            product = ProductService.get_product_info(条码)
            affected = Product.delete(条码)
            if affected > 0:
                logger.info(f"成功删除商品-{product['类别']}: {条码}")
                return True
            logger.warning(f"未找到要删除的商品-{product['类别']}: {条码}")
            return False
        except sqlite3.Error as e:
            logger.error(f"删除商品失败-{product['类别']}: {条码}, 错误: {e}")
            raise ValueError(f"删除商品-{product['类别']}失败，请稍后再试")
    
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
        
    @staticmethod
    def get_book_info(条码):
        book = Book.get_by_barcode(条码)
        if not book:
            logger.warning(f"未找到商品: {条码}")
            return None
        logger.info(f"查询书籍信息: {条码}")
        return {
            '条码': book['条码'],
            '名称': book['名称'],
            '书名': book['书名'],
            '书号': book['书号'],
            '作者': book['作者'],
            '定价': book['定价'],
            '出版社': book['出版社'],
            '出版时间': book['出版时间'],
            '版本号': book['版本号'],
            '译者': book['译者'],
        }
    
    @staticmethod
    def update_product_info(条码, **kwargs):
        try:
            affected = Book.update(条码, **kwargs)
            if affected > 0:
                logger.info(f"成功更新书本: {条码}")
                return True
            logger.warning(f"未更新书本: {条码}, 可能未提供有效更改")
            return False
        except sqlite3.Error as e:
            logger.error(f"更新书法失败: {e}")
            raise ValueError("更新书本信息失败")
    
    def delete_book(条码):        
        try:
            affected = Book.delete(条码)
            if affected > 0:
                logger.info(f"成功删除商品-图书: {条码}")
                return True
            elif affected == -1:
                logger.warning(f"数据不一致：部分表删除失败: {条码}")
                return False
            logger.warning(f"未找到要删除的书本: {条码}")
            return False
        except sqlite3.Error as e:
            logger.error(f"删除商品失败-图书: {条码}, 错误: {e}")
            raise ValueError(f"删除商品-图书失败，请稍后再试")




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