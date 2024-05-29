# routers/groups.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db import schemas, crud
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
)

@router.get("/", response_model=List[schemas.GroupDisplay])
def read_groups(db: Session = Depends(get_db)):
    return crud.get_groups(db)
    

@router.post("/", response_model=schemas.GroupDisplay)
def create_group(request: schemas.GroupBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.create_group(db, request, admin_id=current_user.id)

@router.post("/{group_id}/members", response_model=schemas.GroupMembershipDisplay)
def add_member(group_id: int, request: schemas.GroupMembershipBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return crud.add_group_member(db, group_id, user_id=request.user_id)

#Delete member
@router.delete("{group_id}/members/{member_id}")
def delete_member(member_id: int,  db: Session = Depends(get_db),current_user: schemas.GroupBase = Depends(get_current_user)):
    crud.delete_member(db, member_id)
    return

#Delete Group
@router.delete("/{group_id}/")
def delete_group(group_id: int, db: Session = Depends(get_db),current_user: schemas.GroupBase = Depends(get_current_user)):
    crud.delete_group(db, group_id)
    return
