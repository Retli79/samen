# db/schemas.py

from pydantic import BaseModel
from typing import Optional, List

#Inside user display 
class  User(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class Post(BaseModel):
    id: int
    title: int
    content: str
    class Config:
        orm_mode = True

class FriendRequest(BaseModel):
    id: int
    status: int
    class Config:
        orm_mode = True

class Group(BaseModel):
    id: int
    name: str
    description: str
    class Config:
        orm_mode = True

class GroupMembership(BaseModel):
    id: int
    role: str
    class Config:
        orm_mode = True


##########################


class UserBase(BaseModel):
    username: str
    email: str
    password: str
   


class UserDisplay(UserBase):
    id: int
    is_active: bool
    posts: List['Post'] = []
    friend_requests_sent: List['FriendRequest'] = []
    friend_requests_received: List['FriendRequest'] = []
    friends: List['User'] = []
    groups: List['Group'] = []
    group_memberships: List['GroupMembership'] = []

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str


class PostDisplay(PostBase):
    id: int
    owner_id: int
    owner: User

    class Config:
        orm_mode = True

class FriendRequestBase(BaseModel): 
    id: Optional[int] = None
    sender_id: int
    receiver_id: int
    status: Optional[str] = 'pending'


class FriendRequestDisplay(FriendRequestBase):
    id: int
    status: str
    sender: User
    receiver: User

    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None


class GroupDisplay(GroupBase):
    id: int
    admin_id: int
    admin: User
    members: List['GroupMembership'] = []

    class Config:
        orm_mode = True

class GroupMembershipBase(BaseModel):
    user_id: int
    group_id: int


class GroupMembershipDisplay(GroupMembershipBase):
    id: int
    role: str
    user: User
    group: Group

    class Config:
        orm_mode = True

# Resolve forward references
# User.update_forward_refs()
# Post.update_forward_refs()
# FriendRequest.update_forward_refs()
# Group.update_forward_refs()
# GroupMembership.update_forward_refs()
