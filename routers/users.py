# routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from db import schemas, crud
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


#Create User
@router.post("/")#, response_model=schemas.UserDisplay)
def create_user(request: schemas.UserBase, db: Session = Depends(get_db)):
    return crud.create_user(db, request)
   

#Read one user
@router.get("/{id}", response_model= schemas.UserDisplay)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.get_user(db, id)

#Read all Users
@router.get('/', response_model= List[schemas.UserDisplay])
def get_all_users(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.get_all_users(db)

#Update User
@router.put("/{id}/")
def update_user(id: int, request: schemas.UserBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.update_user(db, id, request)

#Delete User
@router.delete("/{id}/")
def delete_user(id: int, db: Session = Depends(get_db),current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.delete_user(db, id)
