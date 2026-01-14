"""
Performance Optimization Module for ProVerBs Ultimate Brain
- Caching responses
- Request batching
- Async processing
- Memory management
"""

import functools
import hashlib
import json
import time
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class PerformanceCache:
    """In-memory cache with TTL for responses"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
    
    def _generate_key(self, query: str, mode: str, ai_provider: str) -> str:
        """Generate cache key from query parameters"""
        content = f"{query}:{mode}:{ai_provider}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, query: str, mode: str, ai_provider: str) -> Optional[Any]:
        """Get cached response if available and not expired"""
        key = self._generate_key(query, mode, ai_provider)
        
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() < entry['expires']:
                logger.info(f"Cache HIT for query: {query[:50]}...")
                return entry['response']
            else:
                del self.cache[key]
                logger.info(f"Cache EXPIRED for query: {query[:50]}...")
        
        logger.info(f"Cache MISS for query: {query[:50]}...")
        return None
    
    def set(self, query: str, mode: str, ai_provider: str, response: Any):
        """Cache a response with TTL"""
        # If cache is full, remove oldest entry
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        
        key = self._generate_key(query, mode, ai_provider)
        self.cache[key] = {
            'response': response,
            'timestamp': datetime.now(),
            'expires': datetime.now() + timedelta(seconds=self.ttl_seconds)
        }
        logger.info(f"Cached response for query: {query[:50]}...")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl_seconds": self.ttl_seconds,
            "oldest_entry": min([e['timestamp'] for e in self.cache.values()]) if self.cache else None
        }


class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "avg_response_time": 0.0,
            "total_response_time": 0.0,
            "errors": 0
        }
    
    def record_request(self, response_time: float, cached: bool = False, error: bool = False):
        """Record request metrics"""
        self.metrics["total_requests"] += 1
        
        if cached:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1
        
        if error:
            self.metrics["errors"] += 1
        else:
            self.metrics["total_response_time"] += response_time
            self.metrics["avg_response_time"] = (
                self.metrics["total_response_time"] / 
                (self.metrics["total_requests"] - self.metrics["errors"])
            )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        cache_hit_rate = 0.0
        if self.metrics["total_requests"] > 0:
            cache_hit_rate = self.metrics["cache_hits"] / self.metrics["total_requests"] * 100
        
        return {
            **self.metrics,
            "cache_hit_rate": f"{cache_hit_rate:.2f}%"
        }
    
    def reset(self):
        """Reset metrics"""
        self.metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "avg_response_time": 0.0,
            "total_response_time": 0.0,
            "errors": 0
        }


# Global instances
performance_cache = PerformanceCache(max_size=500, ttl_seconds=1800)  # 30 min TTL
performance_monitor = PerformanceMonitor()


def with_caching(func):
    """Decorator to add caching to async functions"""
    @functools.wraps(func)
    async def wrapper(query: str, mode: str, ai_provider: str, *args, **kwargs):
        start_time = time.time()
        
        # Try cache first
        cached_response = performance_cache.get(query, mode, ai_provider)
        if cached_response is not None:
            response_time = time.time() - start_time
            performance_monitor.record_request(response_time, cached=True)
            return cached_response
        
        # Execute function
        try:
            response = await func(query, mode, ai_provider, *args, **kwargs)
            
            # Cache successful response
            performance_cache.set(query, mode, ai_provider, response)
            
            response_time = time.time() - start_time
            performance_monitor.record_request(response_time, cached=False)
            
            return response
        except Exception as e:
            response_time = time.time() - start_time
            performance_monitor.record_request(response_time, cached=False, error=True)
            raise e
    
    return wrapper
