from fastapi import FastAPI
from .router import router

app = FastAPI(title="NCLT Cause List API")
app.include_router(router, prefix="/api")
