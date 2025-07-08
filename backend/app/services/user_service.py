import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User

async def fetch_user_info(access_token: str):
    api_url = 'https://stepik.org/api/stepics/1'  # should be stepic with "c"!
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers={'Authorization': f'Bearer {access_token}'})
        
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch user info")
    
    return response.json().get('users', [])

async def get_or_create_user(stepik_user_info, session: Session):
    if not stepik_user_info:
        raise HTTPException(status_code=400, detail="User information not found")

    user_data = stepik_user_info[0]
    stepik_id = user_data['id']
    
    user = session.query(User).filter_by(stepik_id=stepik_id).first()
    
    if user:
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.avatar = user_data['avatar']
        session.commit()
    else:
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'], 
            avatar=user_data['avatar'], 
            stepik_id=stepik_id
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    return {"sub": user.id}
