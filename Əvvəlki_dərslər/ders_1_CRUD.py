from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app= FastAPI()

class Todo(BaseModel):
    id: int
    title: str
    Done: bool = False
db = []
@app.post("/todos")
def add_todo(todo: Todo):
    db.append(todo)
    return {"mesaj": "Tapşırıq əlavə olundu", "data": todo}
@app.get("/todos")
def get_todos():
    return db
@app.put("/todos/{todo_id}")
def update_todo(todo_id : int, todo_updated: Todo):
    for index, task in enumerate(db) :
        if task.id == todo_id :
            db[index]= todo_updated
            return {"mesaj": "Tapşırıq yeniləndi", "yeni_hal": todo_updated}
    return{"mesaj":"belə id tapılmadı"}
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id : int):
    for task in db :
        if task.id== todo_id:
            db.remove(task)
            return {"mesaj": "Tapşırıq uğurla silindi"}
    return {"mesaj": "Silinəcək tapşırıq tapılmadı"}