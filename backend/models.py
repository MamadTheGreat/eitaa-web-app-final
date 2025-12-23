"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, validator, Field
from typing import Optional, List

class SymptomData(BaseModel):
    """Model for symptom data submission"""
    user_id: str = Field(..., min_length=5, max_length=50)
    symptom_type: str = Field(..., min_length=2, max_length=50)
    value: str = Field(..., min_length=1, max_length=50)

    @validator('user_id')
    def validate_user_id(cls, v):
        if not v.startswith('user_'):
            raise ValueError('Invalid user_id format')
        return v

    @validator('symptom_type')
    def validate_symptom_type(cls, v):
        allowed_types = ['قند ناشتا', 'قند بعد از غذا', 'فشار خون', 'وزن']
        if v not in allowed_types:
            raise ValueError(f'symptom_type must be one of {allowed_types}')
        return v

    @validator('value')
    def validate_value(cls, v, values):
        symptom_type = values.get('symptom_type')
        
        try:
            if symptom_type == 'فشار خون':
                if '/' not in v:
                    raise ValueError('فشار خون باید به فرمت "عدد/عدد" باشد')
                parts = v.split('/')
                systolic = float(parts[0])
                diastolic = float(parts[1])
                
                if not (70 <= systolic <= 250):
                    raise ValueError('فشار سیستولیک باید بین 70 تا 250 باشد')
                if not (40 <= diastolic <= 150):
                    raise ValueError('فشار دیاستولیک باید بین 40 تا 150 باشد')
                if systolic <= diastolic:
                    raise ValueError('فشار سیستولیک باید بزرگتر از دیاستولیک باشد')
            
            elif symptom_type in ['قند ناشتا', 'قند بعد از غذا']:
                value_num = float(v)
                if not (20 <= value_num <= 600):
                    raise ValueError('مقدار قند باید بین 20 تا 600 باشد')
            
            elif symptom_type == 'وزن':
                weight = float(v)
                if not (20 <= weight <= 300):
                    raise ValueError('وزن باید بین 20 تا 300 کیلوگرم باشد')
                    
        except (ValueError, IndexError) as e:
            raise ValueError(f'مقدار نامعتبر: {str(e)}')
        
        return v

class UserHistory(BaseModel):
    """Model for fetching user history"""
    user_id: str = Field(..., min_length=5, max_length=50)
    symptom_filter: Optional[str] = Field(None, max_length=50)

    @validator('user_id')
    def validate_user_id(cls, v):
        if not v.startswith('user_'):
            raise ValueError('Invalid user_id format')
        return v

class VideoResponse(BaseModel):
    """Model for video information"""
    id: str
    name: str
    type: str
    url: str
    size: int

class VideosResponse(BaseModel):
    """Model for list of videos"""
    videos: List[VideoResponse]

class SymptomResponse(BaseModel):
    """Model for symptom save response"""
    success: bool
    message: str
    timestamp: str

class HistoryItem(BaseModel):
    """Model for a single history item"""
    date: str
    time: str
    type: str
    value: str

class HistoryResponse(BaseModel):
    """Model for history response"""
    data: List[HistoryItem]

class ContactInfo(BaseModel):
    """Model for contact information"""
    eitaa: str
    phone: str
    email: str
    address: str

class HealthResponse(BaseModel):
    """Model for health check response"""
    status: str
    services: Optional[dict] = None
    error: Optional[str] = None
    timestamp: str
