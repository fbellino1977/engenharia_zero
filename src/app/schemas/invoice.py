from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.invoice_item import InvoiceItem, InvoiceItemCreate

""" INPUT SCHEMAS (Minimum effort, maximum security) """


class InvoiceCreate(BaseModel):
    user_uuid_id: UUID
    items: list[InvoiceItemCreate] = Field(..., min_length=1)


""" OUTPUT SCHEMAS (Rich in information for the Front-End) """


class Invoice(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    invoice_id: int
    created_at: datetime
    user_id: int
    user_uuid_id: UUID
    items: list[InvoiceItem]
    total_price: float  # Pydantic will read @property of the model
