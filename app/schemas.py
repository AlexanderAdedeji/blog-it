from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime




class ShowUser(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode=True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    



class PostCreate(PostBase):
    pass

    
class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:ShowUser
    class Config:
        orm_mode=True


class ShowPost(PostBase):
    votes:int
class UserCreate(BaseModel):
    email:EmailStr
    password:str


    

class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Vote(BaseModel):
    post_id:int
    direction:int

class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id:Optional[str] =None


