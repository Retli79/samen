# db/crud.py

from sqlalchemy.orm.session import Session
from routers import schemas
from db.hash import Hash
from fastapi import HTTPException, status
from db import models


# User-related operations
def create_user(db: Session, request: schemas.UserBase):
    new_user = models.User(
        username = request.username, 
        email = request.email, 
        password = Hash.bcrypt(request.password)
     )
    test_user = db.query(models.User).filter(models.User.username == new_user.username).first()
    if test_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    test_user = db.query(models.User).filter(models.User.email == new_user.email).first()
    if test_user:
        raise HTTPException(status_code=400, detail="Email already registered")

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

# def get_user_by_email(db: Session, email: str):
#    user = db.query(models.User).filter(models.User.email == email).first()
#    if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#         detail=f"User with email {email} already registered")
#    return user

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