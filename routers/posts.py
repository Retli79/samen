# routers/posts.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import schemas, models, crud
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.post("/", response_model=schemas.PostDisplay)
def create_post( request: schemas.PostBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.create_post(db = db, request = request, owner_id=current_user.id)


@router.get('/{id}', response_model=schemas.PostDisplay) 
def read_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.get_post(db, id) 


@router.get("/", response_model=List[schemas.PostDisplay])
def read_all_posts(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    posts = crud.get_all_posts(db)
    return posts


@router.delete("/{id}/")
def delete_post(id: int, db: Session = Depends(get_db),current_user: schemas.GroupBase = Depends(get_current_user)):
    crud.delete_post(db, id)
    return

