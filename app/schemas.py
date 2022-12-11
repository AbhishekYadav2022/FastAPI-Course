from datetime import datetime
from pydantic import BaseModel, EmailStr

# Base Schema For Post 
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# Schema For Creating Post 
class PostCreate(PostBase):
    pass

# Schema For Getting Post
class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True
        
# Schema For Creating User 
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema For Getting User 
class GetUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    