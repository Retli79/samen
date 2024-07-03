# # routers/friends.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from routers.schemas import FriendRequestBase, FriendRequestDisplay, UserBase
from db.db_friends import create_friend_request, get_friend_requests, accept_friend_request, reject_friend_request
from auth.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix="/friendrequests",
    tags=["friendrequests"],
)

@router.post("/", response_model=FriendRequestDisplay)
def create_request(friend_request: FriendRequestBase, db: Session = Depends(get_db)):
    return create_friend_request(db, friend_request)

@router.get("/{user_id}", response_model=List[FriendRequestDisplay])
def get_requests(user_id: int, db: Session = Depends(get_db)):
    return get_friend_requests(db, user_id)

@router.put("/{request_id}/accept", response_model=FriendRequestDisplay)
def accept_request(request_id: int, receiver_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return accept_friend_request(db, request_id, receiver_id, current_user)

@router.put("/{request_id}/reject", response_model=FriendRequestDisplay)
def reject_request(request_id: int, receiver_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return reject_friend_request(db, request_id, receiver_id, current_user)
