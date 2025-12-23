
# backend/__init__.py
"""
Patient Education API - Backend Package
"""
__version__ = "3.0.0"

# backend/services/__init__.py
"""
Services package - Business logic layer
"""
from .google_drive import drive_service
from .google_sheets import sheets_service
from .cache import cache_service

__all__ = ['drive_service', 'sheets_service', 'cache_service']

# backend/routers/__init__.py
"""
Routers package - API endpoints
"""
from . import education, symptoms, contact

__all__ = ['education', 'symptoms', 'contact']

# backend/middleware/__init__.py
"""
Middleware package
"""
from .rate_limit import RateLimitMiddleware

__all__ = ['RateLimitMiddleware']

# backend/utils/__init__.py
"""
Utils package - Helper functions
"""
from .validators import *
from .logger import setup_logger

__all__ = [
    'validate_blood_sugar',
    'validate_blood_pressure',
    'validate_weight',
    'validate_user_id',
    'validate_disease_type',
    'setup_logger'
]
