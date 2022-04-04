from doctest import Example
from fastapi import APIRouter, Depends, HTTPException,status
from .. import schemas,models,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


rounter = APIRouter(
    tags=['Authentication']
)


@rounter.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    if not utils.verify(user.password,user_credentials.password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    access_token = oauth2.create_token(data = {"user_id": user.id})


    return {"access_token": access_token, "token_type": "Bearer"}
