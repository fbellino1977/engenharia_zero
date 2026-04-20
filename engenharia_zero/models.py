from sqlalchemy import String, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List
from engenharia_zero.database import Base


class UserTable(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    invoices: Mapped[List["InvoiceTable"]] = relationship(back_populates="owner")


class ProductTable(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    # Relationship to invoice items
    invoice_items: Mapped[List["InvoiceItemTable"]] = relationship(
        back_populates="product"
    )


class InvoiceTable(Base):
    __tablename__ = "invoices"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    @property
    def total_price(self):
        return sum(item.unit_price * item.quantity for item in self.items)

    owner: Mapped["UserTable"] = relationship(back_populates="invoices")
    items: Mapped[List["InvoiceItemTable"]] = relationship(back_populates="invoice")


class InvoiceItemTable(Base):
    """N:N Association Table between invoice and product"""

    __tablename__ = "invoice_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[float] = mapped_column(Float)  # Frozen price

    invoice: Mapped["InvoiceTable"] = relationship(back_populates="items")
    product: Mapped["ProductTable"] = relationship(back_populates="invoice_items")
