from typing import Optional
from sqlalchemy.orm.session import Session
from db import models
from routers import schemas
from db.models import User, FriendRequest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models import User, FriendRequest
from routers.schemas import UserBase



# FriendRequest-related operations

def create_friend_request(db: Session, friend_request: schemas.FriendRequestBase):
    add_friend_request = models.FriendRequest(
        sender_id=friend_request.sender_id,
        receiver_id=friend_request.receiver_id,
        status="pending"
    )
    db.add(add_friend_request)
    db.commit()
    db.refresh(add_friend_request)
    return add_friend_request

def update_friend_request(db: Session, friend_request: schemas.FriendRequestBase):
    query = db.query(models.FriendRequest)
    query = query.filter(models.FriendRequest.id == friend_request.id)
    query = query.filter(models.FriendRequest.receiver_id == friend_request.receiver_id)
    query = query.filter(models.FriendRequest.sender_id == friend_request.sender_id)
    query = query.filter(models.FriendRequest.status == "pending")

    db_friend_request = query.first()
    if db_friend_request:
        db_friend_request.status = friend_request.status
        db.commit()
        db.refresh(db_friend_request)
    return db_friend_request

def get_friend_requests(db: Session, user_id: int, status: Optional[str] = None):
    query = db.query(models.FriendRequest).filter(
        (models.FriendRequest.sender_id == user_id) | (models.FriendRequest.receiver_id == user_id)
    )
    if status is not None:
        query = query.filter(models.FriendRequest.status == status)
    
    return query.all()




def accept_friend_request(db: Session, request_id: int, receiver_id: int, current_user: UserBase):
    friend_request = db.query(FriendRequest).filter(
        FriendRequest.id == request_id,
        FriendRequest.receiver_id == receiver_id
    ).first()
    
    if not friend_request:
        raise HTTPException(status_code=404, detail="Friend request not found")
    if friend_request.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only accept friend requests sent to you")
    if friend_request.status != 'pending':
        raise HTTPException(status_code=400, detail="Friend request is not pending")
    
    friend_request.status = "accepted"
    db.commit()
    db.refresh(friend_request)
    add_friend_if_accepted(db, friend_request.sender_id, friend_request.receiver_id)
    return friend_request

def reject_friend_request(db: Session, request_id: int, receiver_id: int, current_user: UserBase):
    friend_request = db.query(FriendRequest).filter(
        FriendRequest.id == request_id,
        FriendRequest.receiver_id == receiver_id
    ).first()
    
    if not friend_request:
        raise HTTPException(status_code=404, detail="Friend request not found")
    if friend_request.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only reject friend requests sent to you")
    if friend_request.status != 'pending':
        raise HTTPException(status_code=400, detail="Friend request is not pending")
    
    friend_request.status = "rejected"
    db.commit()
    db.refresh(friend_request)
    return friend_request


# Friend-related operations

def get_user_friends(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user.friends
    return []

def add_friend_if_accepted(db: Session, user_id: int, friend_id: int):
    friend_request = db.query(FriendRequest).filter(
        FriendRequest.sender_id == user_id,
        FriendRequest.receiver_id == friend_id,
        FriendRequest.status == 'accepted'
    ).first()
    if friend_request:
        user = db.query(User).filter(User.id == user_id).first()
        friend = db.query(User).filter(User.id == friend_id).first()
        if user and friend:
            user.friends.append(friend)
            friend.friends.append(user)
            db.commit()
            return user, friend
    return None

def add_friend(db: Session, user_id: int, friend_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    friend = db.query(User).filter(User.id == friend_id).first()
    if user and friend:
        user.friends.append(friend)
        db.commit()
        return user.friends
    return None

