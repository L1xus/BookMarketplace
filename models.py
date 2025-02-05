from pydantic import BaseModel
from typing import Optional, List
from typing_extensions import Literal
from sqlmodel import Relationship, Field, SQLModel
from sqlalchemy import UniqueConstraint

class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    price: float
    author: str
    pages: Optional[int] = None
    orders: Optional[List["Order"]] = Relationship(back_populates="book")

class Client(SQLModel, table=True):
    __tablename__ = "clients"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    phone: Optional[str] = None
    address: Optional[str] = None
    orders: Optional[List["Order"]] = Relationship(back_populates="client")

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    __table_args__ = (UniqueConstraint("customer_contact"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="books.id")
    client_id: int = Field(foreign_key="clients.id")
    customer_name: str
    customer_contact: str
    status: str = Field(default="pending")
    book: Optional[Book] = Relationship(back_populates="orders")
    client: Optional[Client] = Relationship(back_populates="orders")

class ChatRequest(BaseModel):
    prompt: str

class AiAction(BaseModel):
    action: Literal["add_books", "place_orders", "get_insights"]
    books: Optional[List[Book]] = None
    orders: Optional[List[Order]] = None
    sql_query: Optional[str] = None
