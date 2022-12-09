from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from datetime import date
from random import randrange
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# Schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Welcome to my api!"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

# Get Request


@app.get("/posts")
def get_posts():
    return {"data": "This is your post"}

# Post Request


@app.post("/createposts1")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message": "posted successfully!"}
    # return {"new_post": payload}

# Post Request


@app.post("/createposts")
def create_posts(new_post: Post):
    # Converting pydantic model to dictionary
    print(new_post.dict())
    # print(new_post.rating)
    # print(new_post)
    return {"data": new_post}


# ----------------Doing CRUD Operation------------------#
## ------------------- Get Request---------------##
my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "favourite foods",
        "content": "I like pizza",
        "id": 2
    }
]

@app.get("/allposts")
def get_all_posts():
    return {"data": my_posts}

## ------------------- Post Request---------------##
# Getting Current Time 
today = date.today()
current_date = today.strftime("%d %B, %Y")

## Post Schema 
class PostSchema(BaseModel):
    title: str
    content: str
    date: str = current_date
    author: str = "Admin"

## Post Request 
@app.post("/publishpost", status_code=status.HTTP_201_CREATED)
def publish_post(post: PostSchema):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

## ------------- Get Request With Id ------------##
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
## ----------- Delete Request With Id ----------##
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

# Getting Latest Post 
# @app.get("/post/latest")
# def get_latest_post():
#     latest_post = my_posts[len(my_posts)-1]
#     return {"detail": latest_post}

@app.get("/post/{id}")
def get_post(id: int, response: Response): # Converting id to integer
    post = find_post(id)
    if not post: 
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "No post found"}
        # Or
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    return {"post_detail": post}

## ------------------- Delete Request---------------##
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # Deleting post
    index = find_index_post(id)
    
    # Checking if the post exist 
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    
    my_posts.pop(index)
    return Response(status=status.HTTP_204_NO_CONTENT)
    # return {"message": "Post deleted successfully"} # 204 does not return any content in response
    
## ------------------- Put Request---------------##
@app.put("/posts/{id}")
def update_post(id: int, post: PostSchema):
    index = find_index_post(id)
    
    # Raise Exception
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message": post_dict}