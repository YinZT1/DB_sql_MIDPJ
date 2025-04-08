# from database import init_db
# from utils.logger import setup_logger
# from services.store_service import StoreService
# from services.product_service import ProductService
# from services.customer_service import CustomerService
# from services.sales_service import SalesService

# def main():
#     logger = setup_logger()
#     logger.info("应用程序启动")
    
#     # 初始化数据库
#     try:
#         init_db()
#         logger.info("数据库初始化完成")
#     except Exception as e:
#         logger.error(f"数据库初始化失败: {e}")
#         return
    
#     # 创建服务实例
#     store_service = StoreService()
#     product_service = ProductService()
#     customer_service = CustomerService()
#     sales_service = SalesService()
    
#     # 测试会员注册
#     try:
#         member_id = customer_service.register_member(
#             姓名="王小明",
#             联系电话="13800138000",
#             email="wang@example.com"
#         )
#         print(f"会员注册成功，ID: {member_id}")
        
#         member_info = customer_service.get_member_info(member_id)
#         print(f"会员信息: {member_info}")
#     except Exception as e:
#         print(f"会员操作出错: {e}")
    
#     # 测试销售记录
#     try:
#         # 先确保有门店和商品
#         store_id = store_service.add_store("测试门店", "上海市")
#         product_id = product_service.add_product(
#             条码="TEST001",
#             名称="测试商品",
#             销售价格=10.5,
#             类别="日用品"
#         )
        
#         # 会员购买
#         sale_result = sales_service.create_sale(
#             门店编号=store_id,
#             商品条码=product_id,
#             数量=2,
#             会员电话="13800138000"
#         )
#         print(f"销售成功: {sale_result}")
        
#         # 非会员购买
#         sale_result = sales_service.create_sale(
#             门店编号=store_id,
#             商品条码=product_id,
#             数量=1
#         )
#         print(f"销售成功: {sale_result}")
        
#         # 获取销售报表
#         report = sales_service.get_sales_report()
#         print("销售报表:")
#         print(f"总销售额: {report['总销售额']}")
#         print("按类别统计:")
#         for item in report['按类别统计']:
#             print(f"{item['类别']}: {item['销售额']}元")
#     except Exception as e:
#         print(f"销售操作出错: {e}")

# if __name__ == "__main__":
#     main()
from api.app import create_app
from database import init_db
from utils.logger import setup_logger

def initialize():
    """初始化应用"""
    logger = setup_logger()
    try:
        init_db()
        logger.info("数据库初始化完成")
        return create_app()
    except Exception as e:
        logger.error(f"初始化失败: {e}")
        raise

if __name__ == '__main__':
    app = initialize()
    app.run(host='0.0.0.0', port=5000, debug=True)