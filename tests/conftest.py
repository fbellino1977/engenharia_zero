import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from engenharia_zero.database import Base, get_db

# 1. Define that the test database will be ONLY in RAM (volatile and fast)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# 2. Creates the execution engine for the in-memory database
# StaticPool is vital: it prevents SQLite from deleting data every time a connection closes
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Required for SQLite in memory to maintain data between connections
)

# 3. Creates the session factory (conversations with the database) for testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Prepares the database before each test function
    Scope='function' means: does this for EACH test individually
    """
    # Creates all tables (users, products, invoices) in RAM
    Base.metadata.create_all(bind=engine)  # Setup: Create the tables

    session = TestingSessionLocal()
    try:
        # Deliver the session for the test to use (the test takes place here)
        yield session
    finally:
        # After the test is finished, close the session and DESTROY the tables.
        # This ensures that the next test begins with a 100% clean database
        session.close()
        Base.metadata.drop_all(bind=engine)  # Teardown: Cleans the database


@pytest.fixture(scope="function")
def client(db_session):
    """
    Creates a client that "pretends" to be a browser calling the API, but
    redirecting the real database to the test database
    """

    # This internal function replaces the project's original 'get_db' function
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Inject the replacement: when the API requests a database, FastAPI will deliver the test db_session
    app.dependency_overrides[get_db] = override_get_db

    # Creates the test client to trigger the routes (POST, GET, etc.)
    with TestClient(app) as c:
        yield c

    # Clean the replacement to avoid affecting other processes outside of testing
    app.dependency_overrides.clear()
