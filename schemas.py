from pydantic import BaseModel
from typing import Optional
class UserCreate(BaseModel):
    email: str
    password: str
class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        orm_mode= True

class TodoCreate(BaseModel):
    title: str 
    description: Optional[str]= None 
    done: bool= False
class TodoResponse(BaseModel):
    id: int
    title: str 
    description: Optional[str]= None
    done: bool
class TodoUpdate(BaseModel):
    title: str
    description: Optional[str]= None
    done: bool
   
    class Config:
        orm_mode= True

class UserLogin(BaseModel):
    email: str
    password: str