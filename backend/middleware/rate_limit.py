"""
Rate limiting middleware
"""
from datetime import datetime
from typing import Dict, List
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from config import get_settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting requests"""
    
    def __init__(self, app):
        super().__init__(app)
        self.settings = get_settings()
        self.request_limits: Dict[str, List[float]] = {}
    
    async def dispatch(self, request: Request, call_next):
        """Process request and apply rate limiting"""
        client_ip = request.client.host
        current_time = datetime.now().timestamp()
        
        # Clean old requests
        if client_ip in self.request_limits:
            self.request_limits[client_ip] = [
                req_time for req_time in self.request_limits[client_ip]
                if current_time - req_time < 60
            ]
        
        # Check rate limit
        if client_ip in self.request_limits:
            if len(self.request_limits[client_ip]) >= self.settings.MAX_REQUESTS_PER_MINUTE:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later."
                )
        
        # Record new request
        if client_ip not in self.request_limits:
            self.request_limits[client_ip] = []
        self.request_limits[client_ip].append(current_time)
        
        response = await call_next(request)
        return response
