# main.py

from fastapi import FastAPI
from routers import users, posts, friends, groups, comments, schemas
from db.database import engine
from db import models
from auth import authentication
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(friends.router)
app.include_router(groups.router)
app.include_router(comments.router)

@app.get('/')
def index():
    return {"message": 'Hello World'}


models.Base.metadata.create_all(bind=engine)

app.mount('/images', StaticFiles(directory='images'), name= 'images')
