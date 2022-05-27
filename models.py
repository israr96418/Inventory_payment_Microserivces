from typing import Optional

from sqlmodel import SQLModel, Field


# work both as pydantic and sqlalchemy
class InSchema(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    quantity: int


# work only as a pydantic model for data validaion
class OutSchema(SQLModel):
    name: str
    price: float
    quantity: int
