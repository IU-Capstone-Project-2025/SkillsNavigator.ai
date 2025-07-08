from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
import httpx
import os
from app.config import settings
import jwt
from datetime import datetime, timedelta
from app.services.database import session
from sqlalchemy.orm import Session
from app.services.user_service import fetch_user_info, get_or_create_user 

router = APIRouter(prefix="/api")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/callback")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        print("AAAA", flush=True)
        if user_id is None:
            print("DDD", flush=True)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return user_id
    except jwt.PyJWTError:
        print("CCC", flush=True)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
@router.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"user_id": current_user}

@router.get("/login")
async def get_login_url():
    client_id = os.getenv("CLIENT_ID", "")
    # TODO: get url of app from env
    # WARNING: It should be equal to value from https://stepik.org/oauth2/applications/
    redirect_url = settings.web_url + "/api/callback"
    return f"https://stepik.org/oauth2/authorize/?response_type=code&client_id={client_id}&redirect_uri={redirect_url}"

@router.get("/callback")
async def get_access_token(code: str):
    client_id = os.getenv("CLIENT_ID", "")
    client_secret = os.getenv("CLIENT_SECRET", "")
    redirect_url = f"{settings.web_url}/api/callback"
    
    auth = httpx.BasicAuth(username=client_id, password=client_secret)
    
    async with httpx.AsyncClient(timeout=None, auth=auth) as client:
        token_response = await client.post(
            "https://stepik.org/oauth2/token/",
            params={"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_url}
        )
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=token_response.status_code, detail="Failed to get access token")
        
        access_token = token_response.json().get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="Access token not found in response")

        stepik_user_info = await fetch_user_info(access_token)
        user_data = await get_or_create_user(stepik_user_info, session)

        jwt_token = create_access_token(data=user_data)

        response = RedirectResponse(settings.web_url)
        response.set_cookie(
            key="access_token",
            value=jwt_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=True
        )
        
        return response
        


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt