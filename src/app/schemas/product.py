from pydantic import BaseModel, ConfigDict, Field

""" INPUT SCHEMAS (Minimum effort, maximum security) """


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(gt=0)


""" OUTPUT SCHEMAS (Rich in information for the Front-End) """


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id: int
    name: str
    price: float
