# routers/members.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db import schemas, crud
from db.database import get_db
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/members",
    tags=["groups"],
)

#Delete member
@router.delete("/{member_id}")
def delete_member(member_id: int,  db: Session = Depends(get_db),current_user: schemas.GroupBase = Depends(get_current_user)):
    return crud.delete_member(db, member_id)
