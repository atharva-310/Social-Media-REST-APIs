from fastapi import Depends, HTTPException, status 
from jose import jwt,JWTError
from datetime import datetime,timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from . import models, database
from sqlalchemy.orm import Session
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRATION_TIME = settings.access_token_expire_minutes


def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME)

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate the credentials", headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    return user
