from flask import Blueprint, request, jsonify
from services.sales_service import SalesService
from utils.logger import setup_logger

logger = setup_logger()

bp = Blueprint('sales', __name__, url_prefix='/api/sales')

@bp.route('/', methods=['POST'])
def create_sale():
    """创建销售记录"""
    data = request.get_json()
    required_fields = ['门店编号', '商品条码', '数量']
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必要参数'}), 400
    
    try:
        result = SalesService().create_sale(
            门店编号=data['门店编号'],
            商品条码=data['商品条码'],
            数量=data['数量'],
            会员电话=data.get('会员电话')
        )
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"创建销售记录失败: {e}")
        return jsonify({'error': '创建销售记录失败'}), 500

@bp.route('/report', methods=['GET'])
def get_report():
    """获取销售报表"""
    try:
        report = SalesService().get_sales_report(
            门店编号=request.args.get('门店编号', type=int),
            开始日期=request.args.get('开始日期'),
            结束日期=request.args.get('结束日期')
        )
        return jsonify(report)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"获取销售报表失败: {e}")
        return jsonify({'error': '获取报表失败'}), 500