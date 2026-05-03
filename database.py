import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"
SQLALCEHMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:admin22342@localhost/todo_db"
)


engine = create_engine(SQLALCEHMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()