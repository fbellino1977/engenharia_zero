from pydantic import BaseModel, ConfigDict, Field

from app.schemas.product import Product

""" INPUT SCHEMAS (Minimum effort, maximum security) """


class InvoiceItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


""" OUTPUT SCHEMAS (Rich in information for the Front-End) """


class InvoiceItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    invoice_item_id: int
    invoice_id: int
    product_id: int
    quantity: int
    unit_price: float
    # Upon return, we may want to see the product name
    product: Product | None = None
