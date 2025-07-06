from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
import httpx
import requests
import json
import os
from app.config import settings

router = APIRouter(prefix="/api")


@router.get("/users/me", tags=["users"])
async def read_user_me(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    api_url = 'https://stepik.org/api/stepics/1'  # should be stepic with "c"!
    resp = json.loads(requests.get(api_url, headers={'Authorization': 'Bearer '+ token}).text)

    user = resp['users']
    name = user[0]['first_name'] +' ' + user[0]['last_name']
    return user[0]

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
    redirect_url = settings.web_url + "/api/callback" # why?
    #TODO: Make separate function to update token.
    auth = httpx.BasicAuth(username=client_id, password=client_secret)
    async with httpx.AsyncClient(timeout=None, auth=auth) as client:
        result = await client.post(f"https://stepik.org/oauth2/token/?grant_type=authorization_code&code={code}&redirect_uri={redirect_url}")
        print(result, flush=True)
        access_token = result.json()["access_token"]
        response = RedirectResponse(settings.web_url)
        response.set_cookie(key="access_token", value=access_token, max_age=result.json()["expires_in"], httponly=True, secure=True)
        return response
        # Example of result: {"access_token": "ACCESS_TOKEN", "scope": "read write", "expires_in": 36000, "token_type": "Bearer"}
        