import pytest
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from Inventory_management.main import app, get_db
from Inventory_management.database import Base
from Inventory_management import models   

load_dotenv()

DB_USER = os.getenv("db_user")
DB_PW = os.getenv("db_pw")
DB_HOST = os.getenv("db_host")
DB_PORT = os.getenv("db_port")
TEST_DB_NAME = "inventory_test"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """
    Set up the test database schema once per test session.

    - Creates all tables before any tests run
    - Drops all tables after all tests finish

    This ensures a clean database environment for the entire test run.
    """
    try:
        Base.metadata.create_all(bind=engine)
        yield
    finally:
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    """
    Provide a FastAPI test client with a test database.

    - Overrides the application's `get_db` dependency
    - Injects the test database session instead of real DB
    - Ensures API tests run against isolated test data

    Cleanup:
    - Removes dependency overrides after test
    """
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)
    try:
        yield session

    finally:
        session.close()
        transaction.rollback()   
        connection.close()


@pytest.fixture(scope="function")
def client(db):
    """
    Provides a FastAPI test client using a test database.

    - Overrides get_db dependency to use test DB
    - Yields a TestClient for API testing
    - Clears overrides after test
    """
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    test_client = TestClient(app)

    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()