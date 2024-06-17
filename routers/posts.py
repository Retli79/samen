# routers/posts.py

from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from routers import schemas
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user
import random
import string
import shutil
from db import models, db_post

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

image_url_types = ['absolute', 'relative']

@router.post("/create_post", response_model=schemas.PostDisplay)
def create_post( request: schemas.PostBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Parameter image_url_type can only take values 'absolute' or 'relative'.")
    return db_post.create_post(db = db, request = request, owner_id=current_user.id)


@router.get('/{id}', response_model=schemas.PostDisplay) 
def read_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return db_post.get_post(db, id) 


@router.get("/", response_model=List[schemas.PostDisplay])
def read_posts(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    posts = db_post.get_all_posts(db)
    return posts


@router.delete("/{id}/")
def delete_post(id: int, db: Session = Depends(get_db),current_user: schemas.GroupBase = Depends(get_current_user)):
    db_post.delete_post(db, id)
    return

@router.post('/upload_image')
def upload_image(image: UploadFile = File(...)):
  letters = string.ascii_letters
  rand_str = ''.join(random.choice(letters) for i in range(6))
  new = f'_{rand_str}.'
  filename = new.join(image.filename.rsplit('.', 1))
  path = f'images/{filename}'

  with open(path, "w+b") as buffer:
    shutil.copyfileobj(image.file, buffer)
  
  return {'filename': path}