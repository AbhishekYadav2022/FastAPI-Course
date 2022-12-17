from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint

# Base Schema For Post 
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# Schema For Getting User 
class GetUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
        
# Schema For Creating Post 
class PostCreate(PostBase):
    pass

# Schema For Getting Post
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: GetUser
    
    class Config:
        orm_mode = True
        
# Schema For Creating User 
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
# Schema For Vote 
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)