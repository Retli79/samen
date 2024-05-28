# routers/friends.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from db import schemas, crud
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/friends",
    tags=["friends"],
)

@router.post("/requests", response_model=schemas.FriendRequestDisplay)
def send_friend_request(friend_request: schemas.FriendRequestBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.create_friend_request(db, friend_request)

@router.put("/requests/{id}", response_model=schemas.FriendRequestDisplay)
def read_friend_requests(id: int, friend_request: schemas.FriendRequestBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    if(id != friend_request.id):
        raise HTTPException(status_code=400, detail="The id of the friend request object must be the same as the id in the url")
    if(friend_request.receiver_id != current_user.id):
        raise HTTPException(status_code=403, detail="Can only update friend requests received by you")
    if(friend_request.status == 'pending'):
        raise HTTPException(status_code=400, detail="Cannot update a friend request to pending state, it should be accepted or rejected")
    
    return crud.update_friend_request(db, friend_request)


@router.get("/requests", response_model=List[schemas.FriendRequestDisplay])
def read_friend_requests(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.get_friend_requests(db, user_id=current_user.id)

@router.post("/requests/{request_id}/accept", response_model=schemas.FriendRequestDisplay)
def accept_friend_request(request_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.accept_friend_request(db, request_id, receiver_id=current_user.id)

@router.post("/requests/{request_id}/reject", response_model=schemas.FriendRequestDisplay)
def reject_friend_request(request_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.reject_friend_request(db, request_id=request_id, receiver_id=current_user.id)

@router.get("/", response_model=List[schemas.User])
def read_friends(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.get_friends(db, user_id=current_user.id)
