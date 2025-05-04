from fastapi import APIRouter, Request, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.models import users
from app.db import database
from jose import jwt
from passlib.context import CryptContext
import os

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = os.getenv("SECRET_KEY")
JWT_ALGORITHM = "HS256"

class SignupInput(BaseModel):
    email: EmailStr
    password: str
    invite_code: str  # TODO: replace with secure system

class LoginInput(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
async def signup_user(payload: SignupInput):
    # Fake invite code check
    if payload.invite_code != "SECRET123":
        raise HTTPException(status_code=403, detail="Invalid invite code")

    query = users.select().where(users.c.email == payload.email)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = bcrypt_context.hash(payload.password)
    create_query = users.insert().values(
        email=payload.email,
        hashed_password=hashed_pw,
        is_active=True,
        is_admin=False
    )
    await database.execute(create_query)
    return {"message": "User created successfully. Await admin activation."}

@router.post("/login")
async def login_user(payload: LoginInput):
    query = users.select().where(users.c.email == payload.email)
    user = await database.fetch_one(query)
    if not user or not bcrypt_context.verify(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user["is_active"]:
        raise HTTPException(status_code=403, detail="User not yet approved")

    token = jwt.encode({"user_id": user["id"]}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
