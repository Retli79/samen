from typing import Optional
from sqlalchemy.orm.session import Session
from routers import schemas
from db.hash import Hash
from fastapi import HTTPException, status
from db import models


# FriendRequest-related operations

def create_friend_request(db: Session, friend_request: schemas.FriendRequestBase):
    add_friend_request = models.FriendRequest(sender_id=friend_request.sender_id, receiver_id=friend_request.receiver_id, status="pending")
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
    if friend_request:
        db_friend_request.status = friend_request.status
        db.commit()
        db.refresh(db_friend_request)
    return db_friend_request


def get_friend_requests(db: Session, user_id: int, status: Optional[str]):
    query = db.query(models.FriendRequest).filter((models.FriendRequest.sender_id == user_id) | (models.FriendRequest.receiver_id == user_id))
    if not status == None:
        query = query.filter(models.FriendRequest.status == status)
    
    return query.all()

def accept_friend_request(db: Session, request_id: int, receiver_id: int):
    friend_request = db.query(models.FriendRequest).filter(models.FriendRequest.id == request_id, models.FriendRequest.receiver_id == receiver_id).first()
    if friend_request:
        friend_request.status = "accepted"
        db.commit()
        db.refresh(friend_request)
    return friend_request

def reject_friend_request(db: Session, request_id: int, receiver_id: int):
    friend_request = db.query(models.FriendRequest).filter(models.FriendRequest.id == request_id, models.FriendRequest.receiver_id == receiver_id).first()
    if friend_request:
        friend_request.status = "rejected"
        db.commit()
        db.refresh(friend_request)
    return friend_request

def get_friends(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first() 
    if user:
        return user.friends
    return []