from fastapi import Depends, FastAPI
from . import models
from sqlalchemy.orm import Session
from .routers import post, user,auth,vote
from .database import  get_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
# database.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.rounter)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Api is working "}




@app.get("/testDB")
def get_post (db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts