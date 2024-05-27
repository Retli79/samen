# routers/friends.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db import schemas, crud
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/friends",
    tags=["friends"],
)

@router.post("/requests", response_model=schemas.FriendRequest)
def send_friend_request(friend_request: schemas.FriendRequestBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.create_friend_request(db, friend_request, sender_id=current_user.id)

@router.get("/requests", response_model=List[schemas.FriendRequest])
def read_friend_requests(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.get_friend_requests(db, user_id=current_user.id)

@router.post("/requests/{request_id}/accept", response_model=schemas.FriendRequest)
def accept_friend_request(request_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.accept_friend_request(db, request_id, receiver_id=current_user.id)

@router.post("/requests/{request_id}/reject", response_model=schemas.FriendRequest)
def reject_friend_request(request_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.reject_friend_request(db, request_id=request_id, receiver_id=current_user.id)

@router.get("/", response_model=List[schemas.User])
def read_friends(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.get_friends(db, user_id=current_user.id)
