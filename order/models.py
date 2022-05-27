from typing import Optional

from sqlmodel import SQLModel, Field


# I will used this model as pydantic as well as sqlalchemy
class Product(SQLModel, table=True):
    __name__ = "buy_product"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    quantity: int
