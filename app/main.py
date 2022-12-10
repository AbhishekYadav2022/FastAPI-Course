from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.params import Body
from datetime import date
from random import randrange
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my api!"}

# ----------------Doing CRUD Operation------------------#
## ------------------- Get Request---------------##

@app.get("/posts", response_model=List[schemas.Post])
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

## ------------------- Post Request---------------##

## Post Request 
@app.post("/post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published) # A better way to do this is given below
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

## ------------- Get Request With Id ------------##

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db:Session = Depends(get_db)): # Converting id to integer
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    return post

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
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # Raise Exception
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

# ---------------Users API----------------#
## Post Request API
@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.GetUser)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    # Hashing the password 
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get Request API
@app.get("/users/{id}", response_model=schemas.GetUser)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    # If user not found 
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user