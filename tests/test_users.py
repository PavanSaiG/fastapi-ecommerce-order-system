import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.db import Base
from app.database.session import get_db

# Use test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Ensure fresh DB tables before each test session
@pytest.fixture(autouse=True, scope="module")
def setup_module():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")

def test_create_user():
    response = client.post(
        "/users/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "id" in response.json()

def test_authentication():
    response = client.post(
        "/users/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
