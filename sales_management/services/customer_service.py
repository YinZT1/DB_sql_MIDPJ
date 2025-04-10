from database.models import Customer, Member
from database.db_connector import get_db_connection
from utils.logger import setup_logger
import sqlite3

Logger = setup_logger


class CustomerService:
    """客户服务"""
    
    def __init__(self):
        self.logger = Logger(__name__)

    def register_customer(self, 联系电话, 类型='非会员'):
        """
        注册新客户
        :param 联系电话: 客户电话
        :param 类型: '会员'或'非会员'
        :return: 注册的电话
        """
        try:
            self.logger.info(f"注册客户: {联系电话}({类型})")
        
            # 先检查是否已存在
            existing = Customer.get_by_phone(联系电话)
            if existing:
                # 如果已存在，更新类型
                Customer.update(联系电话, 类型=类型)
                self.logger.info(f"客户已存在，更新类型: {联系电话} -> {类型}")
            else:
                # 如果不存在，创建新客户
                phone = Customer.create(联系电话, 类型)
                self.logger.info(f"客户注册成功: {phone}")
                
            return 联系电话
        except ValueError as e:
            self.logger.error(f"客户注册失败: {str(e)}")
            raise
        except Exception as e:
            self.logger.exception("客户注册异常")
            raise ValueError("客户注册失败")
    
    def upgrade_to_member(self, 姓名, 联系电话, email=None, 地址=None):
        """
        将客户升级为会员
        :param 姓名：客户姓名
        :param 联系电话：客户电话
        :param email：客户email
        :param 地址：客户地址
        :return 会员ID
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                # 开启事务
                conn.execute("BEGIN TRANSACTION")
                
                # 1. 检查客户是否存在
                customer = Customer.get_by_phone(联系电话)
                if not customer:
                    raise ValueError("客户不存在")
                
                # 2. 如果已经是会员，检查是否已有会员记录
                if customer['类型'] == '会员':
                    member = Member.get_by_phone(联系电话)
                    if member:
                        self.logger.warning(f"客户已是会员: {联系电话}")
                        return member['编号']
                
                # 3. 更新客户类型为会员
                Customer.update(联系电话, 类型='会员')
                
                # 4. 创建会员记录
                member_id = Member.create(姓名, 联系电话, email, 地址)
                
                conn.commit()
                self.logger.info(f"升级会员成功: {联系电话} -> 会员ID: {member_id}")
                return member_id
            except Exception as e:
                conn.rollback()
                self.logger.error(f"升级会员失败: {str(e)}")
                raise ValueError(f"升级会员失败: {str(e)}")
            
    def get_customer_info(self, 联系电话):
        """获取客户完整信息(包括会员信息)"""
        try:
            customer = Customer.get_by_phone(联系电话)
            if not customer:
                self.logger.warning(f"客户不存在: {联系电话}")
                return None
                
            result = {
                '联系电话': customer['联系电话'],
                '类型': customer['类型']
            }
            
            if customer['类型'] == '会员':
                member = Member.get_by_phone(联系电话)
                if member:
                    result.update({
                        '会员编号': member['编号'],
                        '姓名': member['姓名'],
                        'email': member['email'],
                        '地址': member['地址']
                    })
            
            self.logger.info(f"查询客户信息: {联系电话}")
            return result
        except Exception as e:
            self.logger.error(f"获取客户信息失败: {str(e)}")
            raise ValueError("获取客户信息失败")
        
    def update_customer(self, 原联系电话, 新联系电话=None, 类型=None):
        """
        更新客户信息
        :param 原联系电话: 原电话
        :param 新联系电话: 新电话(可选)
        :param 类型: 新类型(可选)
        :return: 是否成功
        """
        try:
            affected = Customer.update(原联系电话, 新联系电话, 类型)
            if affected > 0:
                self.logger.info(f"更新客户成功: {原联系电话}")
                return True
            self.logger.warning(f"未更新客户: {原联系电话}")
            return False
        except ValueError as e:
            self.logger.error(f"更新客户验证失败: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"更新客户失败: {str(e)}")
            raise ValueError("更新客户失败")

    def delete_customer(self, 联系电话):
        """
        删除客户(如果是会员会同时删除会员记录)
        :param 联系电话: 要删除的电话
        :return: 是否成功
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                conn.execute("BEGIN TRANSACTION")
                
                # 1. 检查是否是会员
                customer = Customer.get_by_phone(联系电话)
                if not customer:
                    self.logger.warning(f"要删除的客户不存在: {联系电话}")
                    return False
                
                # 2. 如果是会员，先删除会员记录
                if customer['类型'] == '会员':
                    Member.delete_by_phone(联系电话)
                
                # 3. 删除客户记录
                affected = Customer.delete(联系电话)
                
                conn.commit()
                
                if affected > 0:
                    self.logger.info(f"删除客户成功: {联系电话}")
                    return True
                self.logger.warning(f"未删除客户: {联系电话}")
                return False
            except Exception as e:
                conn.rollback()
                self.logger.error(f"删除客户失败: {str(e)}")
                raise ValueError("删除客户失败")


class MemberService:
    """会员专属服务"""
    def __init__(self):
        self.logger = Logger(__name__)
    
    def update_member_info(self, 编号, 姓名=None, email=None, 地址=None):
        """更新会员信息"""
        try:
            affected = Member.update(编号, 姓名, email, 地址)
            if affected > 0:
                self.logger.info(f"更新会员成功: {编号}")
                return True
            self.logger.warning(f"未更新会员: {编号}")
            return False
        except Exception as e:
            self.logger.error(f"更新会员失败: {str(e)}")
            raise ValueError("更新会员失败")

    def get_member_info(self, 编号):
        """获取会员详细信息"""
        try:
            member = Member.get_by_id(编号)
            if not member:
                self.logger.warning(f"会员不存在: {编号}")
                return None
                
            customer = Customer.get_by_phone(member['联系电话'])
            
            return {
                '会员编号': member['编号'],
                '姓名': member['姓名'],
                '联系电话': member['联系电话'],
                'email': member['email'],
                '地址': member['地址']
            }
        except Exception as e:
            self.logger.error(f"获取会员详情失败: {str(e)}")
            raise ValueError("获取会员详情失败")
