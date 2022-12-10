from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

# Using Router 
router = APIRouter()

## Post Request API
@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.GetUser)
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
@router.get("/users/{id}", response_model=schemas.GetUser)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    # If user not found 
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user