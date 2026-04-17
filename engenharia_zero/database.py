from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import String, Integer


# 1. Defining the Base for Alembic and Models
class Base(DeclarativeBase):
    pass


class UserTable(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)


# 2. Engine Configuration and Session Factory
# The 'check_same_thread=False' attribute is a specific SQLite requirement for FastAPI
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Here is the "Factory" that FastAPI will use
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
