# routers/grouprequests.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from routers import schemas
from db import db_groups
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/grouprequests",
    tags=["grouprequests"],
)

@router.post("/", response_model=schemas.GroupRequestDisplay)
def create_group_request(group_request: schemas.GroupRequestBase, db: Session = Depends(get_db)):
    return db_groups.create_group_request(db, group_request)

@router.get("/{user_id}", response_model=List[schemas.GroupRequestDisplay])
def get_group_requests(user_id: int, db: Session = Depends(get_db)):
    return db_groups.get_group_requests(db, user_id)



@router.put("/{request_id}/accept", response_model=schemas.GroupRequestDisplay)
def accept_group_request(request_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    group_request = db_groups.get_group_request_by_id(db, request_id)
    if not group_request:
        raise HTTPException(status_code=404, detail="Group request not found")
    
    group_admin = db_groups.get_group_admin(db, group_request.group_id)
    if not group_admin or group_admin.id != current_user.id:
        raise HTTPException(status_code=403, detail="Only group admins can accept group requests")
    
    if group_request.status != 'pending':
        raise HTTPException(status_code=400, detail="Group request is not pending")
    
    group_request.status = "accepted"
    db.commit()
    db.refresh(group_request)
    db_groups.add_group_member(db, group_request.group_id, group_request.sender_id, role="member")
    return group_request

@router.put("/{request_id}/reject", response_model=schemas.GroupRequestDisplay)
def reject_group_request(request_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    group_request = db_groups.get_group_request_by_id(db, request_id)
    if not group_request:
        raise HTTPException(status_code=404, detail="Group request not found")
    
    group_admin = db_groups.get_group_admin(db, group_request.group_id)
    if not group_admin or group_admin.id != current_user.id:
        raise HTTPException(status_code=403, detail="Only group admins can reject group requests")
    
    if group_request.status != 'pending':
        raise HTTPException(status_code=400, detail="Group request is not pending")
    
    group_request.status = "rejected"
    db.commit()
    db.refresh(group_request)
    return group_request
