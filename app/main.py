from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from datetime import date
from random import randrange
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my api!"}

# ----------------Doing CRUD Operation------------------#
## ------------------- Get Request---------------##

@app.get("/posts")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

## ------------------- Post Request---------------##

## Post Schema 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

## Post Request 
@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db:Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published) # A better way to do this is given below
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

## ------------- Get Request With Id ------------##

@app.get("/posts/{id}")
def get_post(id: int, db:Session = Depends(get_db)): # Converting id to integer
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    return {"post_detail": post}

## ------------------- Delete Request---------------##
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    # Checking if the post exist 
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    post.delete(synchronize_session = False)
    db.commit()
    
# ## ------------------- Put Request---------------##
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # Raise Exception
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}