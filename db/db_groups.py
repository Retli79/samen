# db_groups.py

from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from db import models
from routers import schemas
from db.hash import Hash
from fastapi import HTTPException, status

 
# Group-related operations
 
def create_group(db: Session, request: schemas.GroupBase, admin_id: int):
    add_group = models.Group(
        name = request.name,
        description = request.description,
        admin_id = admin_id
        )
    db.add(add_group)
    db.commit()
    db.refresh(add_group)
    return add_group
 
def get_groups(db: Session):
    return db.query(models.Group).all()
 
def add_group_member(db: Session, group_id: int, user_id: int, role: str = 'member'):
    add_group_membership = models.GroupMembership(
        user_id=user_id,
        group_id=group_id,
        role=role
        )
    db.add(add_group_membership)
    db.commit()
    db.refresh(add_group_membership)
    return add_group_membership
 
def delete_member(db: Session, member_id: int):
    #member = db.query(models.Group).filter(models.Group.id == group_id).first()
    member = db.query(models.GroupMembership).filter(models.GroupMembership.id == member_id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member with id {id} not found")
    if member:
        db.delete(member)
        db.commit()
    return
 
def delete_group(db: Session, group_id: int):
    members = db.query(models.GroupMembership).filter(models.GroupMembership.group_id == group_id).all()
    for member in members:
        delete_member(db, member.id)
   
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group with id {id} not found")
    if group:
        db.delete(group)
        db.commit()
    return







######################################################
def create_group_request(db: Session, group_request: schemas.GroupRequestBase):
    add_group_request = models.GroupRequest(
        sender_id=group_request.sender_id, 
        receiver_id=group_request.receiver_id, 
        group_id=group_request.group_id, 
        status="pending"
    )
    db.add(add_group_request)
    db.commit()
    db.refresh(add_group_request)
    return add_group_request

def update_group_request(db: Session, group_request: schemas.GroupRequestBase):
    query = db.query(models.GroupRequest)
    query = query.filter(models.GroupRequest.id == group_request.id)
    query = query.filter(models.GroupRequest.receiver_id == group_request.receiver_id)
    query = query.filter(models.GroupRequest.status == "pending")

    db_group_request = query.first()
    if not db_group_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group request not found")
    
    db_group_request.status = group_request.status
    if group_request.status == "accepted":
        # Add user to group memberships
        new_membership = models.GroupMembership(
            user_id=group_request.sender_id, 
            group_id=group_request.group_id, 
            role="member"
        )
        db.add(new_membership)
    db.commit()
    db.refresh(db_group_request)
    return db_group_request

def get_group_requests(db: Session, user_id: int):
    return db.query(models.GroupRequest).filter(models.GroupRequest.receiver_id == user_id).all()

def get_group_memberships(db: Session, group_id: int):
    return db.query(models.GroupMembership).filter(models.GroupMembership.group_id == group_id).all()
