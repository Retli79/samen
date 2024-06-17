
#auth/authentication.py

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import models
from db.hash import Hash
from auth import oauth2
from routers import schemas


router = APIRouter(
    tags= ['authentication']
)


@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
    access_token = oauth2.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, 
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username
            }
    

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail='Invalid Credentials')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail='Invalid Credentials')

    access_token = oauth2.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, 
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username
            }
    

@router.post('/register')
def register(request: schemas.UserBase, db: Session = Depends(get_db)):
    new_user = models.User(
        username = request.username, 
        email = request.email, 
        password = Hash.bcrypt(request.password)
     )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

    
