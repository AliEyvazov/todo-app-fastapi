from database import Base 
from sqlalchemy import String, Integer, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True , index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    todos = relationship("TodoDB", back_populates = "owner")

class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    done = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", back_populates = "todos")