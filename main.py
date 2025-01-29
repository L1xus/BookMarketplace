import uvicorn
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session
from database import engine
from crud import (
    add_book_to_db,
    get_books_from_db,
    place_order_in_db,
    get_orders_from_db
)
from models import Book, Order

app = FastAPI()

@app.post("/books/", response_model=Book)
def add_book(book: Book):
    return add_book_to_db(book)

@app.get("/books/", response_model=list[Book])
def get_books():
    return get_books_from_db()

@app.post("/orders/", response_model=Order)
def place_order(order: Order):
    with Session(engine) as session:
        book = session.get(Book, order.book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found!")
    return place_order_in_db(order)

@app.get("/orders/", response_model=list[Order])
def get_orders():
    return get_orders_from_db()


if __name__ == "__main__":
    print(engine)
    SQLModel.metadata.create_all(engine)
    uvicorn.run(app, host="0.0.0.0", port=80)
