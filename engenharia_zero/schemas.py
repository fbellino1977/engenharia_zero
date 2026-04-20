from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from typing import List

""" INPUT SCHEMAS (Minimum effort, maximum security) """


class UserCreate(BaseModel):
    name: str
    age: int = Field(ge=18, le=120)
    email: EmailStr


class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0)


class InvoiceItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class InvoiceCreate(BaseModel):
    user_id: int
    items: List[InvoiceItemCreate] = Field(..., min_length=1)


""" OUTPUT SCHEMAS (Rich in information for the Front-End) """


class Product(BaseModel):
    id: int
    name: str
    price: float
    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class InvoiceItem(BaseModel):
    product_id: int
    quantity: int
    # Upon return, we may want to see the product name
    product: Product | None = None
    model_config = ConfigDict(from_attributes=True)


class Invoice(BaseModel):
    id: int
    created_at: datetime
    user_id: int
    items: List[InvoiceItem]
    total_price: float  # Pydantic will read @property of the model
    model_config = ConfigDict(from_attributes=True)
