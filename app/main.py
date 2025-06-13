# File: backend/app/main.py

from fastapi import FastAPI
from app.routes.auth import auth_router
from app.routes.users import user_router

app = FastAPI(title="OPS Core Secure API")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["User Management"])
from app.db import database
from fastapi import Request

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = database
    response = await call_next(request)
    return response
