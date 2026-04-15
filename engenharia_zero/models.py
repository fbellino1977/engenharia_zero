from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int
    name: str
    age: int = Field(ge=18, le=120)
    email: EmailStr
