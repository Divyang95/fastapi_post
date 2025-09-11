from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional 


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass         

class UserOut(BaseModel):
    id: int
    email: EmailStr 
    created_at: datetime
    name:str

    class Config:
        orm_mode = True



class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int 
    owner: UserOut
    # it is important because as response when give this Post pydantic model as response model 
    # when we do this it then can understand the SQLalchemy model because it can only understand the dictionary or pydantic model
    # but for ORM model we have provid this orm_mode=true so that as response it can also understand SQLAlchemy model
    
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post 
    votes: int 

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email: EmailStr 
    password: str
    name:str 



class UserLogin(BaseModel):
    email:EmailStr 
    password:str 

class Token(BaseModel):
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    id:Optional[int] = None 


class Vote(BaseModel):
    post_id: int 
    dir: conint(ge=0,le=1) 
    