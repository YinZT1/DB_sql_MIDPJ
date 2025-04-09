from flask import Blueprint, request, jsonify
from flask import Response,json
from sales_management.database.db_connector import get_db_connection
from sales_management.services.store_service import StoreService
from utils.logger import setup_logger

logger = setup_logger()
bp = Blueprint('stores', __name__, url_prefix='/api/stores')

@bp.route('/', methods=['GET'])
def get_stores():
    """获取所有门店"""
    try:
        # 实际项目中应该添加分页
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Store")
            stores = [dict(store) for store in cursor.fetchall()]
        
        # 手动处理 JSON 响应，确保中文不转码
        return Response(
            json.dumps(stores, ensure_ascii=False),  # 关键参数
            mimetype='application/json; charset=utf-8'  # 明确指定编码
        )
    
    except Exception as e:
        logger.error(f"获取门店列表失败: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_store():
    """创建新门店"""
    data = request.get_json()
    if not data or '名称' not in data:
        return jsonify({'error': '缺少必要参数'}), 400
    
    try:
        store_id = StoreService.add_store(
            名称=data['名称'],
            地点=data.get('地点'),
            电话=data.get('电话'),
            负责人=data.get('负责人')
        )
        return jsonify({'id': store_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"创建门店失败: {e}")
        return jsonify({'error': '创建门店失败'}), 500

@bp.route('/<int:store_id>', methods=['GET'])
def get_store(store_id):
    """获取指定门店详情"""
    try:
        store = StoreService.get_store_info(store_id)
        if not store:
            return jsonify({'error': '门店不存在'}), 404
        return jsonify(store)
    except Exception as e:
        logger.error(f"获取门店信息失败: {e}")
        return jsonify({'error': str(e)}), 500