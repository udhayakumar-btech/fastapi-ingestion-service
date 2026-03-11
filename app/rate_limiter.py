import threading, time

class RateLimiter:
    def __init__(self, limit, interval):
        self.limit = limit
        self.interval = interval
        self.lock = threading.Lock()
        self.calls = []

    def acquire(self):
        with self.lock:
            now = time.time()
            self.calls = [t for t in self.calls if now - t < self.interval]
            if len(self.calls) >= self.limit:
                sleep_time = self.interval - (now - self.calls[0])
                time.sleep(sleep_time)
            self.calls.append(time.time())
