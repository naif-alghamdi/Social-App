from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

#Base Schema for posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#Creating Post
class PostCreate(PostBase):
    pass

# User Response schemas
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

#POST Response schemas
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    posts: Post
    vote: int 

    class Config:
        orm_mode = True

#Creating User
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)