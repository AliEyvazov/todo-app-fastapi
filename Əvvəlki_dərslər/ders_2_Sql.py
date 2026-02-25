from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# --- 1. BAZA AYARLARI (Database Setup) ---
# Bu fayl yaranacaq: todo.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# Bazanın "mühərriki"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Bazayla əlaqə sessiyası
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bazadakı cədvəllərin şablonu
Base = declarative_base()

# --- 2. BAZA MODELİ (Table) ---
# Bu, SQL bazasında cədvəl yaradır
class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description =Column(String, index=True)
    done = Column(Boolean, default=False)

# Bazanı fiziki olaraq yaradırıq (ilk işə salanda)
Base.metadata.create_all(bind=engine)

# --- 3. PYDANTIC MODELİ (Schema) ---
# Bu, istifadəçidən gələn və gedən məlumatı yoxlayır
class TodoSchema(BaseModel):
    title: str
    description: str
    done: bool = False

# --- 4. TƏTBİQ VƏ FUNKSİYALAR ---
app = FastAPI()

# Bazanı açıb-bağlayan köməkçi funksiya (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINTLƏR (CRUD) ---

# CREATE - Yaratmaq
@app.post("/todos")
def add_todo(todo: TodoSchema, db: Session = Depends(get_db)):
    # Bazaya uyğun yeni obyekt yaradırıq
    new_todo = TodoDB(title=todo.title, description=todo.description, done=todo.done)
    db.add(new_todo)  # Bazaya əlavə et
    db.commit()       # Təsdiqlə (Yaddaşa yaz)
    db.refresh(new_todo) # Yeni ID-ni götür
    return new_todo

# READ - Oxumaq
@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    # Bütün siyahını bazadan oxu
    return db.query(TodoDB).all()

# DELETE - Silmək
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    # Əvvəl tapırıq
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Tapşırıq tapılmadı")
    
    db.delete(todo) # Silirik
    db.commit()     # Təsdiqləyirik
    return {"mesaj": "Silindi"}

# UPDATE - Yeniləmək
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo_yenilenmis: TodoSchema, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Tapşırıq tapılmadı")
    
    todo.description = todo_yenilenmis.description
    todo.title = todo_yenilenmis.title
    todo.done = todo_yenilenmis.done
    db.commit()
    db.refresh(todo)
    return todo         
    