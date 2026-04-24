import uuid
from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from engenharia_zero.models import UserTable, InvoiceTable

# Configurations
DATABASE_URL = "sqlite:///database.db"
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def seed_database():
    session = SessionLocal()

    # 1. Clean old data (optional, be careful in production)
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)

    print("🌱 Seeding database...")

    # 2. Create a Test Admin User
    hashed_pw = pwd_context.hash("Mudar@123")
    user_uuid_id = uuid.uuid4()

    test_user = UserTable(
        user_uuid_id=user_uuid_id,
        name="Fabio Engenheiro",
        email="fabio@exemplo.com",
        telephone="11999999999",
        birth_date=datetime(year=1977, month=11, day=5),
        hashed_password=hashed_pw,
        is_active=True,
        is_admin=True,
    )

    session.add(test_user)
    session.flush()  # For SQLAlchemy to generate the user's 'id' (integer)

    # 3. Create a Test Common User
    hashed_pw = pwd_context.hash("Mudar@123")
    user_uuid_id = uuid.uuid4()

    test_user = UserTable(
        user_uuid_id=user_uuid_id,
        name="Luca Comum",
        email="luca@exemplo.com",
        telephone="11988999988",
        birth_date=datetime(year=2001, month=11, day=8),
        hashed_password=hashed_pw,
        is_active=True,
        is_admin=False,
    )

    session.add(test_user)
    session.flush()  # For SQLAlchemy to generate the user's 'id' (integer)

    # 4. Create a linked test invoice
    test_invoice = InvoiceTable(
        user_id=test_user.user_id,  # Technical FK (Integer)
        user_uuid_id=test_user.user_uuid_id,  # Public FK (UUID)
        created_at=datetime.now(),
    )

    session.add(test_invoice)
    session.commit()

    print(f"Success! User created with UUID: {user_uuid_id}")
    session.close()


if __name__ == "__main__":
    seed_database()
