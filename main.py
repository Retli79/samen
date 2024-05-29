# main.py

from fastapi import FastAPI
from routers import users, posts, friends, groups
from db.database import engine
from db import models
from auth import authentication


app = FastAPI()

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(friends.router)
app.include_router(groups.router)


@app.get('/')
def index():
    return {"message": 'Hello World'}


models.Base.metadata.create_all(bind=engine)


