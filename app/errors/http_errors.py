from fastapi import HTTPException

def http_500(message: str):
    raise HTTPException(status_code=500, detail=message)

def http_400(message: str):
    raise HTTPException(status_code=400, detail=message)

def http_429(message: str = "Too Many Requests"):
    raise HTTPException(status_code=429, detail=message)
