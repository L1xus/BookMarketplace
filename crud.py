from sqlmodel import Session
from models import Book, Order
from database import engine


def add_books_to_db(books):
    if not isinstance(books, list):
        books = [books]

    with Session(engine) as session:
        session.add_all(books)
        session.commit()
    return books

def get_books_from_db():
    with Session(engine) as session:
        books = session.query(Book).all()
    return books

def place_orders_in_db(orders):
    if not isinstance(orders, list):
        orders = [orders]

    with Session(engine) as session:
        session.add_all(orders)
        session.commit()
    return orders

def get_orders_from_db():
    with Session(engine) as session:
        orders = session.query(Order).all()
    return orders
