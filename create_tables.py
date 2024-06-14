from db.database import engine
from db import models

# Import all models here to ensure they are registered
from db.models import User, Post, FriendRequest, Group, GroupMembership, GroupRequest, DbComment

# Create all tables
models.Base.metadata.create_all(bind=engine)

print("All tables created successfully!")
