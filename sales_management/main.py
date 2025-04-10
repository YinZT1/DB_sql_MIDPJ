from database import init_db
from utils.logger import setup_logger
from services.store_service import StoreService
from services.product_service import ProductService
from services.customer_service import CustomerService
from services.sales_service import SalesService

def main():
    logger = setup_logger()
    logger.info("应用程序启动")
    
    # 初始化数据库
    try:
        init_db()
        logger.info("数据库初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        return
    
    # 创建服务实例
    store_service = StoreService()
    product_service = ProductService()
    customer_service = CustomerService()
    member_service = MemberService()
    sales_service = SalesService()
    
    # 测试客户注册
    # 仅用手机号注册为非会员用户
    try:
        # 情况1: 仅用手机号注册为非会员用户
        phone1 = "13700051116"
        customer_service.register_customer(phone1)
        print(f"非会员客户注册成功: {phone1}")
        
        # 情况2: 直接注册为会员用户
        phone2 = "13700051117"
        customer_service.register_customer(phone2, 类型='会员')
        # 然后创建会员记录
        member_id = customer_service.upgrade_to_member(
            姓名="刘会员",
            联系电话=phone2,
            email="liu@example.com"
        )
        print(f"直接注册为会员成功: {phone2}, 会员ID: {member_id}")
        
    except Exception as e:
        print(f"客户注册出错: {e}")

    # 测试非会员用户升级为会员
    try:
        non_member_phone = "13700051116"
        
        customer_info = customer_service.get_customer_info(non_member_phone)
        print(f"\n升级前客户状态 - 电话: {non_member_phone}, 类型: {customer_info['类型']}")
        
        if customer_info['类型'] == '非会员':
            member_id = customer_service.upgrade_to_member(
                姓名="魏会员",
                联系电话=non_member_phone,
                email="wei@example.com",
                地址="上海市"
            )
            print(f"非会员升级为会员成功，ID: {member_id}")
            
            # 验证升级后的状态
            updated_info = customer_service.get_customer_info(non_member_phone)
            print(f"升级后客户状态 - 类型: {updated_info['类型']}")
            print(f"会员详细信息: {member_service.get_member_info(member_id)}")
        else:
            print("该客户已经是会员，无需升级")
            
    except Exception as e:
        print(f"会员升级出错: {e}")
    
    # 测试销售记录
    try:
        # 先确保有门店和商品
        store_id = store_service.add_store("测试门店", "上海市")
        product_id = product_service.add_product(
            条码="TEST001",
            名称="测试商品",
            销售价格=10.5,
            类别="日用品"
        )
        
        # 会员购买
        sale_result = sales_service.create_sale(
            门店编号=store_id,
            商品条码=product_id,
            数量=2,
            会员电话="13800138000"
        )
        print(f"销售成功: {sale_result}")
        
        # 非会员购买
        sale_result = sales_service.create_sale(
            门店编号=store_id,
            商品条码=product_id,
            数量=1
        )
        print(f"销售成功: {sale_result}")
        
        # 获取销售报表
        report = sales_service.get_sales_report()
        print("销售报表:")
        print(f"总销售额: {report['总销售额']}")
        print("按类别统计:")
        for item in report['按类别统计']:
            print(f"{item['类别']}: {item['销售额']}元")
            
    except Exception as e:
        print(f"销售操作出错: {e}")
        
    try:
        
        store_service.delete_store(store_id)
        print(f"门店删除成功: {store_id}")
    except Exception as e:
        print(f"门店删除出错: {e}")

if __name__ == "__main__":
    main()
