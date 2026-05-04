from pydantic import BaseModel, Field

""" INPUT SCHEMAS (Minimum effort, maximum security) """


class PasswordUpdate(BaseModel):
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)


""" OUTPUT SCHEMAS (Rich in information for the Front-End) """
