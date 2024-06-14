# routers/members.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from routers import schemas
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user
from db import db_groups

router = APIRouter(
    prefix="/members",
    tags=["members"],
)
@router.post("/", response_model=schemas.GroupMembershipDisplay)
def add_member(group_id: int, request: schemas.GroupMembershipBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return db_groups.add_group_member(db, group_id, user_id=request.user_id)

#Delete member
@router.delete("/{member_id}")
def delete_member(member_id: int,  db: Session = Depends(get_db),current_user: schemas.GroupBase = Depends(get_current_user)):
    return db_groups.delete_member(db, member_id)
