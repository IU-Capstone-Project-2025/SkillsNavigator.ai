from fastapi import APIRouter

router = APIRouter()

@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}
