import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base


class UserTable(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_uuid_id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, unique=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    telephone: Mapped[str | None] = mapped_column(String(20))
    birth_date: Mapped[datetime] = mapped_column(DateTime)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    invoices: Mapped[list["InvoiceTable"]] = relationship(
        back_populates="owner", foreign_keys="[InvoiceTable.user_id]"
    )


class ProductTable(Base):
    __tablename__ = "products"
    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    # Relationship to invoice items
    invoice_items: Mapped[list["InvoiceItemTable"]] = relationship(
        back_populates="product"
    )


class InvoiceTable(Base):
    __tablename__ = "invoices"
    invoice_id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user_uuid_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.user_uuid_id")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))

    @property
    def total_price(self) -> float:
        return sum(item.unit_price * item.quantity for item in self.items)

    owner: Mapped["UserTable"] = relationship(
        back_populates="invoices", foreign_keys=[user_id]
    )
    items: Mapped[list["InvoiceItemTable"]] = relationship(back_populates="invoice")


class InvoiceItemTable(Base):
    """N:N Association Table between invoice and product"""

    __tablename__ = "invoice_items"
    invoice_item_id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.invoice_id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[float] = mapped_column(Float)  # Frozen price

    invoice: Mapped["InvoiceTable"] = relationship(back_populates="items")
    product: Mapped["ProductTable"] = relationship(back_populates="invoice_items")
