"""
Cache management service
"""
from datetime import datetime
from typing import Optional, Dict, Any
from ..config import get_settings

class CacheService:
    """Simple in-memory cache service"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.settings = get_settings()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        current_time = datetime.now().timestamp()
        
        if current_time - entry['timestamp'] >= self.settings.VIDEO_CACHE_DURATION:
            # Cache expired
            del self._cache[key]
            return None
        
        return entry['data']
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache with current timestamp"""
        self._cache[key] = {
            'data': value,
            'timestamp': datetime.now().timestamp()
        }
    
    def delete(self, key: str) -> None:
        """Delete a key from cache"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cache"""
        self._cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'total_keys': len(self._cache),
            'keys': list(self._cache.keys())
        }

# Global cache instance
cache_service = CacheService()
