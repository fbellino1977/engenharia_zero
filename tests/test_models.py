import pytest
from pydantic import ValidationError
from engenharia_zero.schemas import (
    UserCreate,
    ProductCreate,
    InvoiceItemCreate,
    InvoiceCreate,
)

# --- User ---


def test_user_creation_success():
    # Tests whether a valid User is created correctly
    user = UserCreate(name="Fabio", age="48", email="fabio@exemplo.com")
    assert user.name == "Fabio"


def test_user_creation_invalid_email():
    # Tests whether Pydantic raises the correct error for an invalid email address
    with pytest.raises(ValidationError):
        UserCreate(name="Erro", age="25", email="email-invalido")


def test_user_invalid_age():
    # Tests whether Pydantic raises the correct error for invalid age
    with pytest.raises(ValidationError):
        UserCreate(name="Erro", age=17, email="erro@exemple.com")


# --- Product ---


def test_product_creation_success():
    """Ensures that products with positive prices are accepted"""
    product = ProductCreate(name="Teclado Mecânico", price=250.0)
    assert product.price == 250.0


def test_product_invalid_price():
    """Checks if the system blocks products with zero or negative prices"""
    with pytest.raises(ValidationError):
        ProductCreate(name="Produto Grátis", price=0)

    with pytest.raises(ValidationError):
        ProductCreate(name="Produto Negativo", price=-10.0)


# --- Invoice Items ---


def test_invoice_item_invalid_quantity():
    """Ensures that the quantity of items must be greater than zero"""
    with pytest.raises(ValidationError):
        # Try creating an item with a quantity of zero
        InvoiceItemCreate(product_id=1, quantity=0)


# --- Invoice Testing (Complete Structure) ---


def test_invoice_structure_success():
    """Tests the composition of an invoice with multiple items in the Schema"""
    items = [
        InvoiceItemCreate(product_id=1, quantity=2),
        InvoiceItemCreate(product_id=2, quantity=1),
    ]
    invoice = InvoiceCreate(user_id=1, items=items)

    assert invoice.user_id == 1
    assert len(invoice.items) == 2
    assert invoice.items[0].quantity == 2


def test_invoice_without_items():
    """
    If the Schema requires at least one (optional)
    item, this test validates that requirement
    """
    with pytest.raises(ValidationError):
        # Try creating an invoice with an empty item list
        InvoiceCreate(user_id=1, items=[])
