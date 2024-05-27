# db/schemas.py

from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str
    password: str


class User(UserBase):
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


class Post(PostBase):
    id: int
    owner_id: int
    owner: User

    class Config:
        orm_mode = True

class FriendRequestBase(BaseModel):
    sender_id: int
    receiver_id: int


class FriendRequest(FriendRequestBase):
    id: int
    status: str
    sender: User
    receiver: User

    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None


class Group(GroupBase):
    id: int
    admin_id: int
    admin: User
    members: List['GroupMembership'] = []

    class Config:
        orm_mode = True

class GroupMembershipBase(BaseModel):
    user_id: int
    group_id: int


class GroupMembership(GroupMembershipBase):
    id: int
    role: str
    user: User
    group: Group

    class Config:
        orm_mode = True

# Resolve forward references
User.update_forward_refs()
Post.update_forward_refs()
FriendRequest.update_forward_refs()
Group.update_forward_refs()
GroupMembership.update_forward_refs()
