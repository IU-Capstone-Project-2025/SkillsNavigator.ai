from fastapi import APIRouter, HTTPException, Request, Depends
from app.routers.users import get_current_user
from app.models.roadmap import Dialog, Message
from app.schemas.roadmap import DialogSchema
from app.services.database import session
from pydantic import BaseModel
from sqlalchemy.orm import joinedload
from typing import List


router = APIRouter(prefix="/api")

@router.get("/chats", tags=["chats"], response_model=List[DialogSchema], summary="Get user's chats")
async def get_user_dialogs(current_user: str = Depends(get_current_user)):
    dialogs = session.query(Dialog).options(joinedload(Dialog.messages)).filter(Dialog.owner == current_user).all()
    return dialogs

@router.post("/chats", tags=["chats"], response_model=dict, summary="Create chat")
async def create_dialog(request: Request, current_user: str = Depends(get_current_user)):
    new_dialog = Dialog(name="My way", owner=current_user)

    session.add(new_dialog)
    session.commit()
    session.refresh(new_dialog)

    return {"id": new_dialog.id}
    
class SaveMessageRequest(BaseModel):
    message: str
    messageNumber: int  # You can rename this field if needed

@router.put("/chats/{id}", response_model=dict, tags=["chats"], summary="Save message in some chat")
async def save_message(
    id: int,
    request: SaveMessageRequest,
    current_user: int = Depends(get_current_user),  # Assuming current_user returns user ID
):
    # Check if the dialog exists
    dialog = session.query(Dialog).options(joinedload(Dialog.messages)).filter(Dialog.id == id).first()
    if not dialog:
        raise HTTPException(status_code=404, detail="Dialog not found")

    # Create a new message instance
    new_message = Message(text=request.message, is_user=True, dialog_id=id)
    
    if len(dialog.messages) < 2:
        dialog.name = request.message
    else:
        dialog.name = dialog.messages[1].text

    # Add the new message to the session and commit
    session.add(new_message)
    session.commit()
    session.refresh(new_message)  # Refresh to get the latest state of the object

    # Return a success response
    return {"message": "Message saved successfully", "message_id": new_message.id}