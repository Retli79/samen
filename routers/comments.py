from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from routers import schemas
from routers.schemas import CommentBase
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
def create(request: CommentBase, db: Session = Depends(get_db)):
    return db_comment.create(db, request)

@router.delete('/{comment_id}')
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    comment = db_comment.get_comment_by_id(db, comment_id)
    if comment.username != current_user.username:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this comment.")
    return db_comment.delete_comment(db, comment_id)
