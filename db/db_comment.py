from datetime import datetime
from sqlalchemy.orm import Session
from db.models import DbComment
from routers.schemas import CommentBase
from fastapi import HTTPException, status

def create(db: Session, request: CommentBase):
    new_comment = DbComment(
        text=request.text,
        username=request.username,
        post_id=request.post_id,
        timestamp=datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all(db: Session, post_id: int):
    return db.query(DbComment).filter(DbComment.post_id == post_id).all()

def get_comment_by_id(db: Session, comment_id: int):
    comment = db.query(DbComment).filter(DbComment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id {comment_id} not found")
    return comment

def delete_comment(db: Session, comment_id: int):
    comment = db.query(DbComment).filter(DbComment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id {comment_id} not found")
    db.delete(comment)
    db.commit()
    return
