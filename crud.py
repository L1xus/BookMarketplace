from sqlmodel import Session
from models import Book, Order
from database import engine


def add_book_to_db(book: Book):
    with Session(engine) as session:
        session.add(book)
        session.commit()
    return book

def get_books_from_db():
    with Session(engine) as session:
        books = session.query(Book).all()
    return books

def place_order_in_db(order: Order):
    with Session(engine) as session:
        session.add(order)
        session.commit()
    return order

def get_orders_from_db():
    with Session(engine) as session:
        orders = session.query(Order).all()
    return orders
