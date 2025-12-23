"""
Education endpoints - Video management
"""
from fastapi import APIRouter, HTTPException
from typing import List
from models import VideosResponse, VideoResponse
from services.google_drive import drive_service
from services.cache import cache_service
from utils.validators import validate_disease_type
from utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/api", tags=["education"])

@router.get("/videos/{disease}", response_model=VideosResponse)
async def get_videos(disease: str):
    """
    Get educational videos for a specific disease
    
    - **disease**: Disease type (diabetes, hypertension, cardiac)
    """
    try:
        # Validate disease type
        if not validate_disease_type(disease):
            logger.warning(f"Invalid disease requested: {disease}")
            raise HTTPException(
                status_code=404,
                detail=f"Disease '{disease}' not found"
            )
        
        # Check cache first
        cached_videos = cache_service.get(f"videos_{disease}")
        if cached_videos is not None:
            logger.info(f"Cache hit for disease: {disease}")
            return {"videos": cached_videos}
        
        # Fetch from Google Drive
        videos = drive_service.get_videos_for_disease(disease)
        
        # Cache the results
        cache_service.set(f"videos_{disease}", videos)
        
        logger.info(f"Retrieved {len(videos)} videos for disease: {disease}")
        return {"videos": videos}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching videos: {e}")
        raise HTTPException(
            status_code=500,
            detail="خطا در دریافت ویدیوها"
        )

@router.get("/diseases")
async def get_diseases():
    """
    Get list of available diseases
    """
    from config import get_settings
    settings = get_settings()
    
    diseases = [
        {
            "id": key,
            "name": value,
            "name_fa": {
                "diabetes": "دیابت نوع ۲",
                "hypertension": "فشار خون بالا",
                "cardiac": "بیماری قلبی عروقی"
            }.get(key, value)
        }
        for key, value in settings.DISEASE_FOLDERS.items()
    ]
    
    return {"diseases": diseases}
