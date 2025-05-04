from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

JWT_SECRET = os.getenv("SECRET_KEY")
JWT_ALGORITHM = "HS256"
security_scheme = HTTPBearer()

# Decode JWT
def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Middleware to inject current_user_id for RLS
async def set_rls_context(request: Request):
    credentials: HTTPAuthorizationCredentials = await security_scheme(request)
    token = credentials.credentials
    payload = decode_jwt(token)
    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="User ID missing from token")

    if not hasattr(request.state, "db"):
        raise HTTPException(status_code=500, detail="DB connection not found in request")

    await request.state.db.execute(
        f"SET app.current_user_id = '{int(user_id)}';"
    )
    request.state.user_id = user_id  # Optional: attach to request for reuse
