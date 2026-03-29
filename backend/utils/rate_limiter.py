"""API rate limiting ve retry mekanizması"""

import time
from functools import wraps
from typing import Callable, Any

class RateLimiter:
    """Basit rate limiter"""
    
    def __init__(self, calls_per_second: float = 10):
        """
        Args:
            calls_per_second: Saniyede maksimum çağrı sayısı
        """
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0
    
    def wait(self):
        """Gerekirse bekle"""
        now = time.time()
        elapsed = now - self.last_call
        
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        
        self.last_call = time.time()

def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Hata durumunda retry decorator
    
    Args:
        max_retries: Maksimum deneme sayısı
        delay: İlk bekleme süresi (saniye)
        backoff: Her denemede bekleme çarpanı
    
    Returns:
        Decorator
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        print(f"✗ {func.__name__} başarısız (tüm denemeler): {e}")
                        raise
                    
                    print(f"⚠ {func.__name__} hata (deneme {attempt + 1}/{max_retries}): {e}")
                    print(f"  {current_delay:.1f}s bekleniyor...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            return None
        
        return wrapper
    return decorator

class APIRateLimiter:
    """Çoklu API için rate limiter"""
    
    def __init__(self):
        self.limiters = {}
    
    def get_limiter(self, api_name: str, calls_per_second: float = 10) -> RateLimiter:
        """
        Belirli bir API için rate limiter al
        
        Args:
            api_name: API adı
            calls_per_second: Saniyede maksimum çağrı
        
        Returns:
            RateLimiter instance
        """
        if api_name not in self.limiters:
            self.limiters[api_name] = RateLimiter(calls_per_second)
        
        return self.limiters[api_name]
