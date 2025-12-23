"""
Main FastAPI application
Patient Education API - Version 3.0.0
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from config import get_settings
from middleware.rate_limit import RateLimitMiddleware
from routers import education, symptoms, contact
from services.google_drive import drive_service
from services.google_sheets import sheets_service
from utils.logger import setup_logger

# Setup
settings = get_settings()
logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="API for patient education and symptom tracking"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Rate Limiting Middleware
app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(education.router)
app.include_router(symptoms.router)
app.include_router(contact.router)

# Root endpoint
@app.get("/")
async def root():
    """
    Health check endpoint
    """
    return {
        "message": f"{settings.APP_TITLE} is running",
        "version": settings.APP_VERSION,
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Detailed health check
@app.get("/api/health")
async def health_check():
    """
    Detailed health check with service status
    """
    try:
        # Test Google Drive connection
        _ = drive_service.service
        drive_status = "connected"
    except Exception as e:
        logger.error(f"Drive service error: {e}")
        drive_status = "error"
    
    try:
        # Test Google Sheets connection
        _ = sheets_service.service
        sheets_status = "connected"
    except Exception as e:
        logger.error(f"Sheets service error: {e}")
        sheets_status = "error"
    
    overall_status = "healthy" if (drive_status == "connected" and sheets_status == "connected") else "degraded"
    
    return {
        "status": overall_status,
        "services": {
            "drive": drive_status,
            "sheets": sheets_status
        },
        "version": settings.APP_VERSION,
        "timestamp": datetime.now().isoformat()
    }

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "خطای داخلی سرور",
            "status_code": 500
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup
    """
    logger.info(f"Starting {settings.APP_TITLE} v{settings.APP_VERSION}")
    logger.info(f"CORS origins: {settings.ALLOWED_ORIGINS}")
    logger.info(f"Rate limit: {settings.MAX_REQUESTS_PER_MINUTE} requests/minute")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown
    """
    logger.info("Shutting down application")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
  )
