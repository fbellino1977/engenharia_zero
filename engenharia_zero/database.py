from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# 1. Defining the Base for Alembic and Models
class Base(DeclarativeBase):
    pass


# 2. Engine Configuration and Session Factory
# The 'check_same_thread=False' attribute is a specific SQLite requirement for FastAPI
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Here is the "Factory" that FastAPI will use
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 3. The "magic" of Dependency Injection
# Dependency for FastAPI to obtain a session per request
# This function opens the database, provides the connection to the function, and then closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
