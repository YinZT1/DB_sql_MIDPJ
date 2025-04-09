import uuid
from datetime import datetime
from database.models import Sale, Product, Member
from database.db_connector import get_db_connection
from utils.logger import setup_logger
Logger = setup_logger


class SalesService:
    """销售服务"""
    
    def __init__(self):
        self.logger = Logger(__name__)
    
    def create_sale(self, 门店编号, 商品条码, 数量, 会员电话=None):
        """创建销售记录"""
        try:
            self.logger.info(f"创建销售记录 - 门店:{门店编号} 商品:{商品条码}")
            
            # 获取商品信息
            product = Product.get_by_barcode(商品条码)
            if not product:
                raise ValueError("商品不存在")
            
            # 计算金额
            金额 = float(product['销售价格']) * int(数量)
            
            # 生成唯一单号
            单号 = f"SALE-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
            
            # 检查会员是否存在
            关联客户 = None
            if 会员电话:
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT 1 FROM Member WHERE 联系电话=?
                    """, (会员电话,))
                    if not cursor.fetchone():
                        raise ValueError("会员不存在")
                    关联客户 = 会员电话
            
            # 创建销售记录
            sale_id = Sale.create(
                单号=单号,
                关联门店=门店编号,
                关联商品=商品条码,
                数量=数量,
                金额=金额,
                关联客户=关联客户
            )
            
            self.logger.info(f"销售记录创建成功: {单号}")
            return {
                '单号': 单号,
                '金额': 金额,
                '商品名称': product['名称']
            }
        except ValueError as e:
            self.logger.error(f"销售记录验证失败: {str(e)}")
            raise
        except Exception as e:
            self.logger.exception("创建销售记录异常")
            raise ValueError("创建销售记录失败")

    def get_sales_report(self, 门店编号=None, 开始日期=None, 结束日期=None):
        """获取销售报表"""
        try:
            self.logger.info("生成销售报表")
            
            result = {}
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # 总销售额
                query = "SELECT SUM(金额) as 总销售额 FROM Sale"
                params = []
                
                if 门店编号:
                    query += " WHERE 关联门店=?"
                    params.append(门店编号)
                    if 开始日期:
                        query += " AND 日期 >= ?"
                        params.append(开始日期)
                    if 结束日期:
                        query += " AND 日期 <= ?"
                        params.append(结束日期)
                else:
                    if 开始日期:
                        query += " WHERE 日期 >= ?"
                        params.append(开始日期)
                        if 结束日期:
                            query += " AND 日期 <= ?"
                            params.append(结束日期)
                    elif 结束日期:
                        query += " WHERE 日期 <= ?"
                        params.append(结束日期)
                
                cursor.execute(query, params)
                result['总销售额'] = cursor.fetchone()['总销售额'] or 0
                
                # 按类别统计
                query = """
                    SELECT p.类别, SUM(s.金额) as 销售额, SUM(s.数量) as 销售数量
                    FROM Sale s
                    JOIN Product p ON s.关联商品 = p.条码
                """
                if 门店编号 or 开始日期 or 结束日期:
                    query += " WHERE "
                    conditions = []
                    if 门店编号:
                        conditions.append("s.关联门店=?")
                    if 开始日期:
                        conditions.append("s.日期 >= ?")
                    if 结束日期:
                        conditions.append("s.日期 <= ?")
                    query += " AND ".join(conditions)
                
                query += " GROUP BY p.类别"
                cursor.execute(query, params)
                result['按类别统计'] = cursor.fetchall()
            
            return result
        except Exception as e:
            self.logger.error(f"生成销售报表失败: {str(e)}")
            raise ValueError("生成销售报表失败")