from routers import schemas
from routers.schemas import CommentBase
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_comment
from auth.oauth2 import get_current_user


router = APIRouter(
  prefix='/comments',
  tags=['comments']
)

@router.get('/')
def comments(post_id: int, db: Session = Depends(get_db)):
  return db_comment.get_all(db, post_id)


@router.post('')
def create(request: CommentBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
  if not request.username == current_user.username:
    raise HTTPException(403, "Cannot create a comment for someone else")
  
  return db_comment.create(db, request)