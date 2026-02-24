import time


class RateLimiter:
    def __init__(self, requests_per_second=2):
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0
        
    def wait(self):
        """Ждет необходимое время перед следующим запросом"""
        elapsed = time.time() - self.last_request_time
        sleep_time = max(0, self.min_interval - elapsed)
        
        if sleep_time > 0:
            time.sleep(sleep_time)
            
        self.last_request_time = time.time()