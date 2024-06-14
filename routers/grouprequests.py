# routers/groups.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from routers import schemas
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user
from db import db_groups

router = APIRouter(
    prefix="/grouprequests",
    tags=["grouprequests"],
)

@router.post("/", response_model=schemas.GroupRequestDisplay)
def send_group_request(group_request: schemas.GroupRequestBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return db_groups.create_group_request(db, group_request)

@router.put("/{id}/", response_model=schemas.GroupRequestDisplay)
def accept_or_deny_group_requests(id: int, group_request: schemas.GroupRequestBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    if id != group_request.id:
        raise HTTPException(status_code=400, detail="The id of the group request object must be the same as the id in the url")
    if group_request.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only update group requests received by you")
    if group_request.status == 'pending':
        raise HTTPException(status_code=400, detail="Cannot update a group request to pending state, it should be accepted or rejected")
    
    return db_groups.update_group_request(db, group_request)

@router.get("/", response_model=List[schemas.GroupRequestDisplay])
def read_group_requests(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return db_groups.get_group_requests(db, user_id=current_user.id)