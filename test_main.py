from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db =TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
def test_health_check_qapisi():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mesaj": "API tam qaydasinda isleyir"}
def test_istifadeci_yaratmaq():
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "sifre"}
    )
    assert response.status_code in [200,201]
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
def test_tam_giris_ve_todo_yaratmaq():
    response_qeyd = client.post(
        "/users/",
        json={"email": "test2@example.com", "password": "sifre"}
    )
    assert response_qeyd.status_code in [200,201]
    response_login = client.post(
        "/login/",
        json={"email": "test2@example.com", "password": "sifre"}
    )
    assert response_login.status_code == 200
    token = response_login.json()["access_token"]
    assert token is not None

    basliqlar = {
        "Authorization": f"Bearer {token}"
    }
    response_todo = client.post(
        "/todos/",
        json={"title": "Pytest Todo", "description": "bu Todo testdir"},
        headers= basliqlar
    )
    assert response_todo.status_code in [200,201]
    assert response_todo.json()["title"] == "Pytest Todo"