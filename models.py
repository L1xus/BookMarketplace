from pydantic import BaseModel
from typing import Optional, List
from sqlmodel import Relationship, Field, SQLModel
from sqlalchemy import UniqueConstraint

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    price: float
    author: str
    pages: Optional[int] = None
    orders: Optional[List["Order"]] = Relationship(back_populates="book")

class Order(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("customer_contact"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    customer_name: str
    customer_contact: str
    status: str = Field(default="pending")
    book: Optional[Book] = Relationship(back_populates="orders")

class AiAction(BaseModel):
    action: str
    books: Optional[List[dict]] = None
    orders: Optional[List[dict]] = None
