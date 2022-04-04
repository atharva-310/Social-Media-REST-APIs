
from datetime import datetime
import email

from typing import Optional
from pydantic import BaseModel, EmailStr, conint

#requests models 
class PostIn(BaseModel):
    title: str
    content: str
    published : bool = True

class create_user(BaseModel):
    email: EmailStr
    password: str

class login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

    class config: 
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[str] = None

class User():
    id: str
    email: EmailStr

class Vote(BaseModel):
    post_id: int 
    dir: conint(le=1)



#response models

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

    
class PostOut(PostIn):
    pass
    id : int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True


class PostOutF(BaseModel):
    Post: PostOut
    votes: int
    
    class Config:
        orm_mode  = True
