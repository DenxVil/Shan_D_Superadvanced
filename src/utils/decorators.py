"""
Utility Decorators for Shan-D
Created by: ◉Ɗєиνιℓ 
Performance, logging, and functionality decorators
"""
import asyncio
import time
import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)

def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure function execution time"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.debug(f"⏱️ {func.__name__} executed in {execution_time:.4f}s")
        return result
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.debug(f"⏱️ {func.__name__} executed in {execution_time:.4f}s")
        return result
    
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

def error_handler(fallback_value: Any = None):
    """Decorator to handle errors gracefully"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"❌ Error in {func.__name__}: {e}")
                return fallback_value
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"❌ Error in {func.__name__}: {e}")
                return fallback_value
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator

def rate_limit(max_calls: int = 10, time_window: int = 60):
    """Rate limiting decorator"""
    call_history = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_time = time.time()
            func_name = func.__name__
            
            if func_name not in call_history:
                call_history[func_name] = []
            
            # Clean old calls
            call_history[func_name] = [
                call_time for call_time in call_history[func_name]
                if current_time - call_time < time_window
            ]
            
            # Check rate limit
            if len(call_history[func_name]) >= max_calls:
                logger.warning(f"🚫 Rate limit exceeded for {func_name}")
                raise Exception(f"Rate limit exceeded for {func_name}")
            
            call_history[func_name].append(current_time)
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def cache_result(ttl: int = 300):  # 5 minutes default
    """Simple caching decorator"""
    cache = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
            current_time = time.time()
            
            # Check if cached result exists and is still valid
            if cache_key in cache:
                cached_time, cached_result = cache[cache_key]
                if current_time - cached_time < ttl:
                    return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache[cache_key] = (current_time, result)
            
            return result
        
        return wrapper
    
    return decorator
