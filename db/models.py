# db/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

friends_table = Table(
    'friends',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('friend_id', Integer, ForeignKey('users.id'))
)

# models.py

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    
    posts = relationship('Post', back_populates='owner')
    friend_requests_sent = relationship('FriendRequest', foreign_keys='FriendRequest.sender_id', back_populates='sender')
    friend_requests_received = relationship('FriendRequest', foreign_keys='FriendRequest.receiver_id', back_populates='receiver')
    friends = relationship('User', secondary=friends_table, primaryjoin=id==friends_table.c.user_id, secondaryjoin=id==friends_table.c.friend_id, back_populates='friends')
    groups = relationship('Group', back_populates='admin')
    group_memberships = relationship('GroupMembership', back_populates='user')
    group_requests_sent = relationship('GroupRequest', foreign_keys='GroupRequest.sender_id', back_populates='sender')
    group_requests_received = relationship('GroupRequest', foreign_keys='GroupRequest.receiver_id', back_populates='receiver')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    image_url_type = Column(String)
    caption = Column(String)
    title = Column(String, index=True)
    content = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    owner = relationship('User', back_populates='posts')
    comments = relationship('DbComment', back_populates='post')

class FriendRequest(Base):
    __tablename__ = 'friend_requests'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, default='pending')
    
    sender = relationship('User', foreign_keys=[sender_id], back_populates='friend_requests_sent')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='friend_requests_received')

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    admin_id = Column(Integer, ForeignKey('users.id'))
    
    admin = relationship('User', back_populates='groups')
    members = relationship('GroupMembership', back_populates='group')

class GroupMembership(Base):
    __tablename__ = 'group_memberships'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    role = Column(String, default='member')
    
    user = relationship('User', back_populates='group_memberships')
    group = relationship('Group', back_populates='members')

############################

# models.py

class GroupRequest(Base):
    __tablename__ = 'group_requests'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    status = Column(String, default='pending')
    
    sender = relationship('User', foreign_keys=[sender_id], back_populates='group_requests_sent')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='group_requests_received')
    group = relationship('Group')

class DbComment(Base):
    __tablename__ = 'comments'
   
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='comments')
 
