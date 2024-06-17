# main.py

from fastapi import FastAPI
from routers import users, posts, friends, groups, comments, members, grouprequests
from db.database import engine
from db import models
from auth import authentication
from  fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(friends.router)
app.include_router(members.router)
app.include_router(groups.router)
app.include_router(grouprequests.router)
app.include_router(comments.router)

@app.get('/')
def index():
    return {"message": 'Hello World'}


models.Base.metadata.create_all(bind=engine)

app.mount('/images', StaticFiles(directory='images'), name= 'images')

# Add CORS middleware to allow all origins and methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
    allow_headers=["*"],
)