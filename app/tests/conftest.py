
import os

os.environ.setdefault("SECRET_KEY", "chave-secreta-apenas-para-testes")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest
from fastapi.testclient import TestClient
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app            
from database import Base, get_db  
from models.users import User         

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _login(client, email, password):
    r = client.post("/auth/login", data={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture()
def user_headers(client):
    client.post("/auth/register", json={"email": "user@test.com", "password": "123456"})
    return _login(client, "user@test.com", "123456")


@pytest.fixture()
def admin_headers(client, db):
    client.post("/auth/register", json={"email": "admin@test.com", "password": "123456"})
    u = db.query(User).filter_by(email="admin@test.com").first()
    u.role = "admin"        
    db.commit()
    return _login(client, "admin@test.com", "123456")