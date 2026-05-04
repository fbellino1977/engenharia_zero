import uuid
from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import from app package
from app.db.models import InvoiceTable, UserTable

# Configurations
# Note: In Docker, this will be overridden by environment variables
DATABASE_URL = "sqlite:///./data/database.db"
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def seed_database():
    session = SessionLocal()

    print("🌱 Seeding database...")

    # 2. Creates the default admin user
    if (
        not session.query(UserTable)
        .filter(UserTable.email == "fabio@exemplo.com")
        .first()
    ):
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
        session.flush()

    # 5. Create a Test Common User
    if (
        not session.query(UserTable)
        .filter(UserTable.email == "luca@exemplo.com")
        .first()
    ):
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
        session.flush()

        # 4. Create a linked test invoice
        test_invoice = InvoiceTable(
            user_id=test_user.user_id,
            user_uuid_id=test_user.user_uuid_id,
            created_at=datetime.now(),
        )

        session.add(test_invoice)
        session.commit()

        print(f"Success! User created with UUID: {user_uuid_id}")
        session.close()


if __name__ == "__main__":
    seed_database()
