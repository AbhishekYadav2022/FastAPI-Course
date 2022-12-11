from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from datetime import date
from random import randrange
from .. import models, schemas
from ..database import engine, get_db
from sqlalchemy.orm import Session

# Using Router 
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# ----------------Doing CRUD Operation------------------#
## ------------------- Get Request---------------##

@router.get("/", response_model=List[schemas.Post])
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

## ------------------- Post Request---------------##

## Post Request 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published) # A better way to do this is given below
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

## ------------- Get Request With Id ------------##

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db:Session = Depends(get_db)): # Converting id to integer
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    return post

## ------------------- Delete Request---------------##
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    # Checking if the post exist 
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    post.delete(synchronize_session = False)
    db.commit()
    
# ## ------------------- Put Request---------------##
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # Raise Exception
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()