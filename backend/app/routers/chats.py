from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
import httpx
import requests
import json
import os
from app.config import settings

router = APIRouter(prefix="/api")


@router.get("/users/me", tags=["chats"])
async def read_user_me(request: Request):
    
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    api_url = 'https://stepik.org/api/stepics/1'  # should be stepic with "c"!
    resp = json.loads(requests.get(api_url, headers={'Authorization': 'Bearer '+ token}).text)

    user = resp['users']
    name = user[0]['first_name'] +' ' + user[0]['last_name']
    return user[0]
