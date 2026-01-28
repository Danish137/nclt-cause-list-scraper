import time

_cache = {}

def set_cache(key, value, ttl=60):
    _cache[key] = (value, time.time() + ttl)

def get_cache(key):
    if key not in _cache:
        return None
    value, exp = _cache[key]
    if time.time() > exp:
        del _cache[key]
        return None
    return value
