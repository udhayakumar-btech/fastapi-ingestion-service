import requests
from .rate_limiter import RateLimiter

global_limiter = RateLimiter(limit=10, interval=60)  # 10 requests/minute
provider_limiters = {
    "api1": RateLimiter(limit=5, interval=60),
    "api2": RateLimiter(limit=5, interval=60),
    "api3": RateLimiter(limit=5, interval=60),
}

def fetch_with_limit(provider, url, timeout=5):
    global_limiter.acquire()
    provider_limiters[provider].acquire()
    resp = requests.get(url, timeout=timeout, verify=False)
    resp.raise_for_status()
    return resp.json()
