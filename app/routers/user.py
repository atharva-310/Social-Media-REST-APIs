from msilib import schema
from fastapi import APIRouter,HTTPException,Depends,status
from .. import schemas,models,utils
from ..database import get_db
from sqlalchemy.orm import Session

from app import database

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/")
def create_users(user: schemas.create_user, db: Session= Depends(get_db)):
    check_user = db.query(models.User).filter(models.User.email == user.email).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_306_RESERVED, detail="Email address already exists")
    #hashing the password 
    hash_password  = utils.hash(user.password)
    user.password = hash_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"email" : new_user.email, "id" : new_user.id}

@router.get("/{id}",response_model=schemas.UserOut)
def check_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"User with the id-{id} not found")
    return user

