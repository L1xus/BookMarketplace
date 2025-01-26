from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    price: float
    author: str
    pages: Optional[int] = None


class Order(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("customer_contact"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    customer_name: str
    customer_contact: str
    status: str = Field(default="pending")
