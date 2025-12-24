"""
Validation utility functions
"""
from typing import Optional

def validate_blood_sugar(value: str) -> Optional[str]:
    """Validate blood sugar value"""
    try:
        num = float(value)
        if not (20 <= num <= 1500):
            return 'مقدار قند باید بین 20 تا 1500 باشد'
        return None
    except ValueError:
        return 'مقدار قند نامعتبر است'

def validate_blood_pressure(systolic: str, diastolic: str) -> Optional[str]:
    """Validate blood pressure values"""
    try:
        sys = float(systolic)
        dia = float(diastolic)
        
        if not (70 <= sys <= 300):
            return 'فشار سیستولیک باید بین 70 تا 300 باشد'
        if not (30 <= dia <= 200):
            return 'فشار دیاستولیک باید بین 30 تا 200 باشد'
        if sys <= dia:
            return 'فشار سیستولیک باید بزرگتر از دیاستولیک باشد'
        return None
    except ValueError:
        return 'فشار خون نامعتبر است'

def validate_weight(value: str) -> Optional[str]:
    """Validate weight value"""
    try:
        num = float(value)
        if not (10 <= num <= 200):
            return 'وزن باید بین 10 تا 200 کیلوگرم باشد'
        return None
    except ValueError:
        return 'وزن نامعتبر است'

def validate_user_id(user_id: str) -> bool:
    """Validate user_id format"""
    return user_id.startswith('user_') and len(user_id) >= 5

def validate_disease_type(disease: str) -> bool:
    """Validate disease type"""
    from ..config import get_settings
    settings = get_settings()
    return disease in settings.DISEASE_FOLDERS
