from sqlalchemy.orm.session import Session
from routers import schemas
from db.hash import Hash
from fastapi import HTTPException, status
from db import models
import datetime

# Post-related operations


def create_post(db: Session, request: schemas.PostBase, owner_id: int):
    new_post = models.Post(
    image_url = request.image_url,
    image_url_type = request.image_url_type,
    caption = request.caption,
    title = request.title,
    content = request.content,
    owner_id = request.owner_id,
    created_at = datetime.datetime.now()
        )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print("-------------------------------",new_post)
    return new_post


def get_all_posts(db: Session):
    return db.query(models.Post).all()


def get_post(db:Session, id: int):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with id {id} not found")
    return post

def delete_post(db: Session, id: int):
    post = db.query(models.Post).filter(models.Post.id == id).first() 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post:
        db.delete(post)
        db.commit()
    return 