from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# List of domains that can talk to our api 
# origins = ["https://www.wikipedia.org/"]
origins = ["*"] # All domains are allowed 

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods = ["*"], # All methods are allowed
    allow_headers = ["*"] # All headers are allowed
)

@app.get("/")
def root():
    return {"message": "Welcome to my api!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)