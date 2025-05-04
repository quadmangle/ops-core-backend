from app.security import set_rls_context

@router.get("/me")
async def get_my_user(request: Request):
    await set_rls_context(request)
    # now any query respects RLS automatically
    return {"user_id": request.state.user_id}
from fastapi import APIRouter, Request, Depends, HTTPException
from app.security import set_rls_context
from app.models import users
from app.db import database

user_router = APIRouter()

@user_router.get("/me", summary="Get my user profile")
async def get_my_profile(request: Request):
    # Set RLS context using JWT
    await set_rls_context(request)

    query = users.select().where(users.c.id == request.state.user_id)
    user = await database.fetch_one(query)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user["id"],
        "email": user["email"],
        "is_active": user["is_active"],
        "is_admin": user["is_admin"]
    }
