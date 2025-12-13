from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

def get_ip_key(request: Request):
    return get_remote_address(request) or "127.0.0.1"

limiter = Limiter(key_func=get_ip_key)
