from datetime import datetime, date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

""" AUTHENTICATION """


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: Optional[str] = None


""" INPUT SCHEMAS (Minimum effort, maximum security) """


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telephone: Optional[str] = Field(None, max_length=20)
    birth_date: datetime
    password: str = Field(..., min_length=8)

    @field_validator("birth_date")
    @classmethod
    def validate_age(cls, v: datetime) -> datetime:
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))

        if age < 18:
            raise ValueError("O usuário deve ter pelo menos 18 anos")
        if age > 120:
            raise ValueError("Data de nascimento inválida (idade máxima 120 anos)")
        return v


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(gt=0)


class InvoiceItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class InvoiceCreate(BaseModel):
    user_uuid_id: UUID
    items: List[InvoiceItemCreate] = Field(..., min_length=1)


""" OUTPUT SCHEMAS (Rich in information for the Front-End) """


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id: int
    name: str
    price: float


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    user_uuid_id: UUID
    name: str
    email: EmailStr
    telephone: Optional[str]
    birth_date: datetime
    is_active: bool
    is_admin: bool


class InvoiceItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    invoice_item_id: int
    invoice_id: int
    product_id: int
    quantity: int
    unit_price: float
    # Upon return, we may want to see the product name
    product: Product | None = None


class Invoice(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    invoice_id: int
    created_at: datetime
    user_id: int
    user_uuid_id: UUID
    items: List[InvoiceItem]
    total_price: float  # Pydantic will read @property of the model
