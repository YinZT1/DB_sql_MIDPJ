from database.models import Store
from utils.logger import setup_logger
import sqlite3
logger = setup_logger()


class StoreService:
    """门店服务"""
    
    @staticmethod
    def add_store(名称, 地点=None, 电话=None, 负责人=None):
        try:
            store_id = Store.create(名称, 地点, 电话, 负责人)
            logger.info(f"成功添加门店: {名称}, ID: {store_id}")
            return store_id
        except sqlite3.Error as e:
            logger.error(f"添加门店失败: {e}")
            raise ValueError("添加门店失败，请检查数据是否正确")
    
    @staticmethod
    def get_store_info(编号):
        store = Store.get_by_id(编号)
        if not store:
            logger.warning(f"未找到门店: {编号}")
            return None
        
        logger.info(f"查询门店信息: {编号}")
        return {
            '编号': store['编号'],
            '名称': store['名称'],
            '地点': store['地点'],
            '电话': store['电话'],
            '负责人': store['负责人']
        }
    
    @staticmethod
    def update_store_info(编号, **kwargs):
        try:
            affected = Store.update(编号, **kwargs)
            if affected > 0:
                logger.info(f"成功更新门店: {编号}")
                return True
            logger.warning(f"未更新门店: {编号}, 可能未提供有效更改")
            return False
        except sqlite3.Error as e:
            logger.error(f"更新门店失败: {e}")
            raise ValueError("更新门店信息失败")