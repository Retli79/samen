# routers/groups.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from routers import schemas
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user
from db import db_groups

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
)

@router.get("/", response_model=List[schemas.GroupDisplay])
def read_groups(db: Session = Depends(get_db)):
    return db_groups.get_groups(db)
    

@router.post("/", response_model=schemas.GroupDisplay)
def create_group(request: schemas.GroupBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return db_groups.create_group(db, request, admin_id=current_user.id)

#Delete Group
@router.delete("/{group_id}/")
def delete_group(group_id: int, db: Session = Depends(get_db),current_user: schemas.GroupBase = Depends(get_current_user)):
    db_groups.delete_group(db, group_id)
    return
