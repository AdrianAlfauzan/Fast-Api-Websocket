from datetime import datetime, timedelta
import logging
from fastapi import APIRouter, Depends, HTTPException, Form
from app.middleware import jwt
from app.middleware.jwt import jwt_middleware, oauth2_bearer
from app.repositories.token import RevokedToken
from app.services.auth import AuthService
from app.schemas.user_mgt import AuthUser,UserRegister
from typing import Annotated
from app.core.config import settings
from jose import jwt 
from pytz import timezone
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

router = APIRouter()
auth_service = AuthService()

@router.post("/auth/register")
def register(body: UserRegister):
    return {"message": auth_service.register_user(body)}

@router.post("/auth/login")
def auth_get_access_token(
    username: str = Form(...),
    password: str = Form(...)
):
    access_token = auth_service.generate_token(username, password)
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60*60*24,  
        samesite="lax",    
        secure=False      
    )
    return response

@router.get("/auth/me")
def auth_get_me(auth_user: Annotated[AuthUser, Depends(jwt_middleware)]):
    user_data = auth_service.get_user_details(auth_user.id)
    return user_data

@router.post("/auth/logout")
def logout(auth_user: Annotated[AuthUser, Depends(jwt_middleware)], token: str = Depends(oauth2_bearer)):
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    RevokedToken.add(token)
    return {"message": "Logout successful. Token has been revoked."}

@router.post("/auth/api-token")
def generate_api_token  (auth_user: AuthUser = Depends(jwt_middleware)):
    """
    Generate a token for API usage with a short expiration time.
    """
    try:
        # Gunakan zona waktu Indonesia
        indonesia_tz = timezone("Asia/Jakarta")
        current_time = datetime.now(indonesia_tz)
        expire = current_time + timedelta(minutes=5)

        # Generate payload menggunakan data dari `auth_user`
        payload = {
            "id": auth_user.id,
            "company_id": auth_user.company_id,
            "full_name": auth_user.full_name,
            "username": auth_user.username,
            "email": auth_user.email,
            "roles": auth_user.roles,
            # "company_name": getattr(auth_user, "company_name", "Unknown Company"),
            "exp": int(expire.timestamp()),  # Expiration as Unix timestamp
            "expires": expire.isoformat()    # ISO format for human-readable expiration
        }

        # Encode token menggunakan jose.jwt
        api_token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

        return {"api_token": api_token, "type": "Bearer"}
    except Exception as e:
        logging.error(f"Error in generate_api_token: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating API token: {str(e)}")