# routers/members.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from routers import schemas
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user
from db import db_groups, models

router = APIRouter(
    prefix="/members",
    tags=["members"],
)

def is_admin(db: Session, group_id: int, user_id: int):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if group.admin_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    return True

@router.post("/", response_model=schemas.GroupMembershipDisplay)
def add_member(group_id: int, request: schemas.GroupMembershipBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    is_admin(db, group_id, current_user.id)  # Check if current user is admin
    return db_groups.add_group_member(db, group_id, user_id=request.user_id)

@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    member = db.query(models.GroupMembership).filter(models.GroupMembership.id == member_id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    is_admin(db, member.group_id, current_user.id)  # Check if current user is admin of the group
    return db_groups.delete_member(db, member_id)

@router.get("/{group_id}", response_model=List[schemas.GroupMembershipDisplay])
def get_members(group_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return db_groups.get_group_memberships(db, group_id)
