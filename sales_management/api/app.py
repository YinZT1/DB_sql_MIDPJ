from flask import Flask
from flask_cors import CORS
from sales_management.api.routes import stores, sales
from utils.logger import setup_logger

logger = setup_logger()

def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)
    CORS(app)  # 允许跨域请求
    
    # 配置
    app.config['JSON_AS_ASCII'] = False  # 确保中文正常显示
    app.config['JSON_SORT_KEYS'] = False  # 保持JSON字段顺序
    
    # 注册蓝图
    app.register_blueprint(stores.bp)
    app.register_blueprint(sales.bp)
    @app.route('/')
    def app_idx():
        return "hello here homepage"

    @app.route('/api/health')
    def health_check():
        """健康检查端点"""
        return {'status': 'healthy', 'message': '销售管理系统API运行正常'}
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404错误: {error}")
        return {'error': '资源未找到'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500错误: {error}")
        return {'error': '服务器内部错误'}, 500
    
    logger.info("Flask应用初始化完成")
    return app
