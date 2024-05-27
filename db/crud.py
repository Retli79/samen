# db/crud.py

from sqlalchemy.orm.session import Session
from db import models, schemas
from db.hash import Hash
from fastapi import HTTPException, status



# User-related operations
def create_user(db: Session, request: schemas.UserBase):
    new_user = models.User(
        username = request.username, 
        email = request.email, 
        password = Hash.bcrypt(request.password)
     )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
   return  db.query(models.User).all()
   

def get_user(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

def get_user_by_username(db: Session, username: str):
   user = db.query(models.User).filter(models.User.username == username).first()
   if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"User with username {username} not found")
   return user

def update_user(db: Session, id:int, request: schemas.UserBase):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    if user:
        user.username = request.username
        user.email = request.email
        user.password = Hash.bcrypt(request.password)
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
                            
    if user:
        db.delete(user)
        db.commit()
    return user



     

# Post-related operations


def create_post(db: Session, request: schemas.PostBase, owner_id: int):
    new_post = models.Post(
        **request.dict(),
        owner_id=owner_id        
        )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all_posts(db: Session):
    return db.query(models.Post).all()


def get_post(db:Session, id: int):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with id {id} not found")
    return post

# FriendRequest-related operations

def create_friend_request(db: Session, friend_request: schemas.FriendRequest, sender_id: int):
    add_friend_request = models.FriendRequest(**friend_request.dict(), sender_id=sender_id, status="pending")
    db.add(add_friend_request)
    db.commit()
    db.refresh(add_friend_request)
    return add_friend_request

def get_friend_requests(db: Session, user_id: int):
    return db.query(models.FriendRequest).filter((models.FriendRequest.sender_id == user_id) | (models.FriendRequest.receiver_id == user_id)).all()

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

# Group-related operations

def create_group(db: Session, request: schemas.GroupBase, admin_id: int):
    add_group = models.Group(
        name = request.name,
        description = request.description,
        admin_id = admin_id
        )
    db.add(add_group)
    db.commit()
    db.refresh(add_group)
    return add_group

def get_groups(db: Session):
    return db.query(models.Group).all()

def add_group_member(db: Session, group_id: int, user_id: int, role: str = 'member'):
    add_group_membership = models.GroupMembership(
        user_id=user_id, 
        group_id=group_id, 
        role=role
        )
    db.add(add_group_membership)
    db.commit()
    db.refresh(add_group_membership)
    return add_group_membership
