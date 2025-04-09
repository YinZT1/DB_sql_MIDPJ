import re
from datetime import datetime

class DataValidator:
    """数据验证工具"""
    
    @staticmethod
    def validate_phone(phone):
        """验证联系电话格式"""
        return bool(re.match(r'^1[3-9]\d{9}$', phone))
    
    @staticmethod
    def validate_email(email):
        """验证邮箱格式"""
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

class DataConverter:
    """数据转换工具"""
    
    @staticmethod
    def format_date(date_str, input_format='%Y-%m-%d', output_format='%Y年%m月%d日'):
        """日期格式转换"""
        try:
            date_obj = datetime.strptime(date_str, input_format)
            return date_obj.strftime(output_format)
        except ValueError:
            return date_str
    
    @staticmethod
    def dict_to_object(data_dict, obj_class):
        """字典转模型对象"""
        return obj_class(**{
            k: v for k, v in data_dict.items() 
            if hasattr(obj_class, k)
        })

class StatisticsUtils:
    """统计计算工具"""
    
    @staticmethod
    def calculate_growth(current, previous):
        """计算增长率"""
        if previous == 0:
            return float('inf') if current > 0 else 0
        return round((current - previous) / previous * 100, 2)
    
    @staticmethod
    def paginate(data_list, page=1, per_page=10):
        """简单分页处理"""
        start = (page - 1) * per_page
        end = start + per_page
        return data_list[start:end]