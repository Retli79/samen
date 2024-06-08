# routers/groups.py

from fastapi import APIRouter, Depends
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

@router.post("/{group_id}/members", response_model=schemas.GroupMembershipDisplay)
def add_member(group_id: int, request: schemas.GroupMembershipBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return db_groups.add_group_member(db, group_id, user_id=request.user_id)

#Delete member
@router.delete("{group_id}/members/{member_id}")
def delete_member(member_id: int,  db: Session = Depends(get_db),current_user: schemas.GroupBase = Depends(get_current_user)):
    db_groups.delete_member(db, member_id)
    return

#Delete Group
@router.delete("/{group_id}/")
def delete_group(group_id: int, db: Session = Depends(get_db),current_user: schemas.GroupBase = Depends(get_current_user)):
    db_groups.delete_group(db, group_id)
    return


@router.post("/group-requests", response_model=schemas.GroupRequestDisplay)
def send_group_request(group_request: schemas.GroupRequestBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return db_groups.create_group_request(db, group_request)

@router.put("/group-requests/{id}/", response_model=schemas.GroupRequestDisplay)
def accept_or_deny_group_requests(id: int, group_request: schemas.GroupRequestBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    if id != group_request.id:
        raise HTTPException(status_code=400, detail="The id of the group request object must be the same as the id in the url")
    if group_request.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only update group requests received by you")
    if group_request.status == 'pending':
        raise HTTPException(status_code=400, detail="Cannot update a group request to pending state, it should be accepted or rejected")
    
    return db_groups.update_group_request(db, group_request)

@router.get("/group-requests", response_model=List[schemas.GroupRequestDisplay])
def read_group_requests(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return db_groups.get_group_requests(db, user_id=current_user.id)