from database import Base 
from sqlalchemy import String, Integer, Column, Boolean
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True , index=True)
    hashed_password = Column(Integer)
    is_active = Column(Boolean, default=True)

class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    done = Column(Boolean, default=False)