from database.models import Member
from utils.logger import setup_logger
import sqlite3
Logger = setup_logger


class CustomerService:
    """客户服务"""
    
    def __init__(self):
        self.logger = Logger(__name__)
    
    def register_member(self, 姓名, 联系电话, email=None, 地址=None):
        """注册新会员"""
        try:
            self.logger.info(f"尝试注册会员: {姓名}({联系电话})")
            
            if not 姓名 or not 联系电话:
                raise ValueError("姓名和联系电话不能为空")
            
            member_id = Member.create(姓名, 联系电话, email, 地址)
            self.logger.info(f"会员注册成功，ID: {member_id}")
            return member_id
        except ValueError as e:
            self.logger.error(f"会员注册失败: {str(e)}")
            raise
        except Exception as e:
            self.logger.exception("会员注册出现异常")
            raise ValueError("会员注册过程中出现错误")

    def get_member_info(self, 会员编号):
        """获取会员信息"""
        try:
            member = Member.get_by_id(会员编号)
            if not member:
                self.logger.warning(f"未找到会员: {会员编号}")
                return None
                
            self.logger.info(f"查询会员信息: {会员编号}")
            return {
                '编号': member['编号'],
                '姓名': member['姓名'],
                '联系电话': member['联系电话'],
                'email': member['email'],
                '地址': member['地址'],
                '类型': member['类型']
            }
        except Exception as e:
            self.logger.error(f"获取会员信息失败: {str(e)}")
            raise ValueError("获取会员信息失败")