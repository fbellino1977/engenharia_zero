from sqlalchemy import select
from datetime import datetime
from engenharia_zero import models, schemas


def test_create_user_db(db_session):
    """Tests the simple persistence of an user in the test database"""
    # 1. Preparation (using the Input Schema)
    user_in = schemas.UserCreate(
        name="Aline",
        email="aline@exemplo.com",
        telephone="1144410954",
        birth_date="1986-05-13T00:00:00",
        password="Mudar@123",
    )

    # 2. Execution (Converting to the SQLAlchemy Model)
    new_user = models.UserTable(
        name=user_in.name,
        email=user_in.email,
        telephone=user_in.telephone,
        birth_date=user_in.birth_date,
        hashed_password=user_in.password,
    )
    db_session.add(new_user)
    db_session.commit()

    # 3. Verification
    query = select(models.UserTable).where(
        models.UserTable.email == "aline@exemplo.com"
    )
    retrieved_user = db_session.scalar(query)

    assert retrieved_user is not None
    assert retrieved_user.name == "Aline"
    assert (
        retrieved_user.user_id is not None
    )  # Ensures that the database generated the PK


def test_create_invoice_with_items_db(db_session):
    """Tests the N:N relationship and invoice integrity in the database"""
    # 1. Setup: A user and a product are required to prevent the FK from failing
    user = models.UserTable(
        name="Comprador",
        email="comprador@test.com",
        telephone="1173828653",
        birth_date=datetime.strptime("2003-07-16", "%Y-%m-%d"),
        hashed_password="Mudar@123",
    )
    product = models.ProductTable(name="Monitor", price=1200.0)
    db_session.add_all([user, product])
    db_session.commit()

    # 2. Create the Invoice
    new_invoice = models.InvoiceTable(user_id=user.user_id)
    db_session.add(new_invoice)
    db_session.flush()  # Generates the invoice ID

    # 3. Creates the Invoice Item (Relationship)
    new_item = models.InvoiceItemTable(
        invoice_id=new_invoice.invoice_id,
        product_id=product.product_id,
        quantity=2,
        unit_price=product.price,
    )
    db_session.add(new_item)
    db_session.commit()
    db_session.refresh(new_invoice)

    # 4. Composition Verification
    assert len(new_invoice.items) == 1
    assert new_invoice.items[0].product.name == "Monitor"
    assert new_invoice.items[0].quantity == 2
