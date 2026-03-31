from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import security
import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() :
    db = SessionLocal()
    try:
        yield db 
    finally: 
        db.close()
@app.post("/users", response_model = schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user=db.query(models.UserDB).filter(models.UserDB.email== user.email).first()
    if db_user:
        raise HTTPException(status_code = 400, detail ="Bu email artıq qeydiyyatdan keçib")
    
    hashed_pwd = security.get_password_hash(user.password)
    new_user = models.UserDB(
        email = user.email,
        hashed_password = hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
# CREATE
# @app.post("/todos", response_model = schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
# def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
#     new_todo = models.TodoDB(
#         title=todo.title,
#         description=todo.description,
#         done=todo.done
#     )
#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
#     return new_todo
# # Read ALL
# @app.get("/todos",response_model = List[schemas.TodoResponse])
# def read_todos(db: Session = Depends(get_db)):
#     todos=db.query(models.TodoDB).all()
#     return todos
# # Read ONE
# @app.get("/todos/{id}",response_model= schemas.TodoResponse)
# def read_todos(id: int , db: Session = Depends(get_db)):
#     todo=db.query(models.TodoDB).filter(models.TodoDB.id == id).first()
#     if not todo :
#         raise HTTPException(status_code=404,detail = "Tapşırıq tapılmadı")
#     return todo
# # DELETE
# @app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_todo(id: int, db: Session = Depends(get_db)):
#     todo=db.query(models.TodoDB).filter(models.TodoDB.id==id).first()
#     if not todo :
#         raise HTTPException( status_code=404, detail ="Tapşırıq tapılmadı")
#     db.delete(todo)
#     db.commit()
#     return None
# @app.put("/todos/{id}", response_model = schemas.TodoResponse)
# def update_todo(id: int, new_todo: schemas.TodoCreate ,db: Session = Depends(get_db)) :
#     todo = db.query(models.TodoDB).filter(models.TodoDB.id == id).first()
#     if not todo :
#         raise HTTPException(status_code=404,detail="Tapşırıq tapılmadı")
#     todo.title = new_todo.title
#     todo.description = new_todo.description
#     todo.done = new_todo.done
#     db.commit()
#     db.refresh(todo)
#     return todo
@app.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.UserDB).filter(models.UserDB.email == user_credentials.email).first()
    if not user or not security.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email və ya parol səhvdir"
        )
    access_token = security.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}
@app.get("/profile")
def get_profile(token: str = Depends(security.oauth2_scheme), db: Session = Depends(get_db)):

    email = security.verify_token(token)
    user = db.query(models.UserDB).filter(models.UserDB.email == email).first()

    return {
        "mesaj": "Təbriklər! Sən qorunan qapıdan içəri keçdin.",
        "istifadeci_maili": user.email
    }
@app.post("/todos")
def create_todo(
    todo: schemas.TodoCreate,
    token: str = Depends(security.oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = security.verify_token(token)
    user = db.query(models.UserDB).filter(models.UserDB.email == email).first()

    new_todo = models.TodoDB(
        title = todo.title,
        description = todo.description,
        owner_id = user.id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo
@app.get("/todos")
def get_todo(
    token: str = Depends(security.oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = security.verify_token(token)
    user = db.query(models.UserDB).filter(models.UserDB.email == email).first()
    todos = db.query(models.TodoDB).filter(models.TodoDB.owner_id == user.id).all()

    return todos
@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    token: str = Depends(security.oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = security.verify_token(token)
    user = db.query(models.UserDB).filter(models.UserDB.email == email).first()
    todo = db.query(models.TodoDB).filter(models.TodoDB.id == todo_id, models.TodoDB.owner_id == user.id).first()

    if todo is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Tapşırıq tapılmadı və ya bu tapşırığı silməyə icazəniz yoxdur"
        )
    
    db.delete(todo)
    db.commit()
    return {"mesaj": f"{todo_id} nömrəli tapşırıq uğurla silindi!"}
@app.put("/todos/{todo_id}")
def update_todo(
    todo_id: str,
    todo_update: schemas.TodoUpdate,
    token: str = Depends(security.oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = security.verify_token(token)
    user = db.query(models.UserDB).filter(models.UserDB.email == email).first()
    todo = db.query(models.TodoDB).filter(models.TodoDB.id == todo_id, models.TodoDB.owner_id == user.id).first()
    if todo is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Tapşırıq tapılmadı və ya bu tapşırığı yeniləməyə icazəniz yoxdur"
        )
    todo.title = todo_update.title
    todo.description = todo_update.description
    todo.done = todo_update.done

    db.commit()
    db.refresh(todo)
    return todo