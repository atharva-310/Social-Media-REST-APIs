
from typing import List
from sqlalchemy import func
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model=List[schemas.PostOutF])
def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    
    if not posts:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="No posts found")
    
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    
    return results

@router.post("/",status_code= status.HTTP_201_CREATED, response_model= schemas.PostOut)
def create_post(post: schemas.PostIn, db: Session= Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model= schemas.PostOut)
def find_post(id: int,db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db :Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "post not found")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session= False)
    db.commit()
    return{"message": "The post is deleted successfully"}