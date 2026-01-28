import time
from ..errors.http_errors import http_429

class RateLimiter:
    def __init__(self, rate=5, per=10):
        self.capacity = rate
        self.tokens = rate
        self.per = per
        self.last = time.time()

    def allow(self):
        now = time.time()
        elapsed = now - self.last
        self.last = now
        self.tokens = min(self.capacity, self.tokens + elapsed * (self.capacity / self.per))
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


limiter = RateLimiter(rate=5, per=10)
