from typing import Optional, List
from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

# Using Router 
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# ----------------Doing CRUD Operation------------------#
## ------------------- Get Request---------------##

@router.get("/", response_model=List[schemas.Post])

# To Get All The Posts Of The Current User 
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() 
#     return posts
    
# To Get All The Posts 
def get_posts(db: Session = Depends(get_db), limit: int = 20, skip: int = 0, search: Optional[str] = ""):
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # Offset is used to skip some results # Filter is used to search or filter posts 
    return posts

## ------------------- Post Request---------------##

## Post Request 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published) # A better way to do this is given below
    # print(current_user.email)
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
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
def delete_post(id: int, db:Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    # Checking if the post exist 
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete")
    
    post_query.delete(synchronize_session = False)
    db.commit()
    
# ## ------------------- Put Request---------------##
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # Raise Exception
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete")
    
    db.commit()
    return post_query.first()