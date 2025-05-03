# File: backend/app/main.py

try:
    from fastapi import FastAPI
    from app.routes.auth import auth_router
    from app.routes.users import user_router
except ModuleNotFoundError as e:
    raise ImportError("Critical dependency missing. Ensure FastAPI and its dependencies like 'ssl' are properly installed in your environment.") from e

app = FastAPI(title="OPS Core Secure API")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["User Management"])
