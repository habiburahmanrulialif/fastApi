import asyncio
import pytest
from httpx import AsyncClient
from main import app, get_db
from models import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "postgresql+asyncpg://postgres:test123@172.18.0.1:5432/test_feedbackDb"

# Create an async engine and session maker
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module", autouse=True)
async def create_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_clean_all_tables():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Make a POST request to the /clean endpoint
        response = await client.post("/clean")
        
        # Check if the response status code is 200
        assert response.status_code == 200
        
        # Check if the response message is correct
        assert response.json() == {"message": "All tables have been cleaned successfully"}

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/register", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_login_for_access_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/register", json={"username": "testuser2", "password": "testpassword2"})
        response = await ac.post("/token", data={"username": "testuser2", "password": "testpassword2"})
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_create_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        token_response = await ac.post("/token", data={"username": "testuser", "password": "testpassword"})
        token = token_response.json()["access_token"]
        response = await ac.post("/items", json={"title": "testitem"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "testitem"

@pytest.mark.asyncio
async def test_create_feedback_rating():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        token_response = await ac.post("/token", data={"username": "testuser", "password": "testpassword"})
        token = token_response.json()["access_token"]
        item_response = await ac.post("/items", json={"title": "testitem2"}, headers={"Authorization": f"Bearer {token}"})
        item_id = item_response.json()["id"]
        response = await ac.post("/feedback", json={"item_id": item_id, "rating": 4}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["rating"] == 4

@pytest.mark.asyncio
async def test_get_feedback_ratings():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        token_response = await ac.post("/token", data={"username": "testuser", "password": "testpassword"})
        token = token_response.json()["access_token"]
        item_response = await ac.post("/items", json={"title": "testitem3"}, headers={"Authorization": f"Bearer {token}"})
        item_id = item_response.json()["id"]
        await ac.post("/feedback", json={"item_id": item_id, "rating": 5}, headers={"Authorization": f"Bearer {token}"})
        response = await ac.get(f"/feedback/{item_id}")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["rating"] == 5
