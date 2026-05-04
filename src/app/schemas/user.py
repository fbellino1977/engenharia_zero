from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

""" INPUT SCHEMAS (Minimum effort, maximum security) """


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telephone: str | None = Field(None, max_length=20)
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


""" OUTPUT SCHEMAS (Rich in information for the Front-End) """


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    user_uuid_id: UUID
    name: str
    email: EmailStr
    telephone: str | None
    birth_date: datetime
    is_active: bool
    is_admin: bool
