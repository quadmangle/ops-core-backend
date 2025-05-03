## Phase 1: Backend + DB Secure Skeleton (FastAPI + PostgreSQL + OPS Core Ready)

# Directory: /backend/app/

# main.py
from fastapi import FastAPI
from app.routes.auth import auth_router
from app.routes.users import user_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])

# /backend/app/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.security import create_jwt_token, verify_invite_code

class LoginInput(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

auth_router = APIRouter()

@auth_router.post("/login", response_model=TokenResponse)
def login(data: LoginInput):
    # TODO: Add hashed password verification
    if data.email == "admin@example.com":
        token = create_jwt_token(user_id=1, role="admin")
        return TokenResponse(access_token=token)
    raise HTTPException(status_code=401, detail="Invalid credentials")

# /backend/app/routes/users.py
from fastapi import APIRouter, Depends
from app.models import User
from app.security import get_current_admin_user

user_router = APIRouter()

@user_router.get("/", dependencies=[Depends(get_current_admin_user)])
def list_users():
    return ["admin@example.com"]  # TODO: Fetch from DB

# /backend/app/security.py
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends

SECRET_KEY = "REPLACE_ME_SECURELY"
ALGORITHM = "HS256"


def create_jwt_token(user_id: int, role: str):
    exp = datetime.utcnow() + timedelta(hours=2)
    return jwt.encode({"sub": str(user_id), "role": role, "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_admin_user():
    # TODO: Extract token from header, validate it, ensure admin
    return True


def verify_invite_code(code: str):
    if code != "SECRET_INVITE":
        raise HTTPException(status_code=403, detail="Invalid invite code")

# /backend/app/models.py
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool
    created_at: str

# Note: The following SQL schema should be placed in a separate migration script or SQL file.
# Example: schema.sql or using Alembic for SQLAlchemy migrations

"""
-- SQL: schema.sql
-- users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role TEXT CHECK (role IN ('admin', 'user')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row-Level Security:
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY select_own_record ON users FOR SELECT USING (id = current_user_id());
"""
