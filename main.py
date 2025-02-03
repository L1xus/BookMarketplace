import os
import time
import uvicorn
import instructor
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session
from database import engine
from crud import (
    add_books_to_db,
    get_books_from_db,
    place_orders_in_db,
    get_orders_from_db,
)
from models import Book, Order, AiAction
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = instructor.from_openai(OpenAI(api_key=OPENAI_API_KEY))

app = FastAPI()

@app.post("/books/", response_model=list[Book])
def add_books(books: list[Book] | Book):
    return add_books_to_db(books)


@app.get("/books/", response_model=list[Book])
def get_books():
    return get_books_from_db()


@app.post("/orders/", response_model=list[Order])
def place_orders(orders: list[Order] | Order):
    with Session(engine) as session:
        if isinstance(orders, list):
            for order in orders:
                book = session.get(Book, order.book_id)
                if not book:
                    raise HTTPException(status_code=404, detail=f"Book with ID {order.book_id} not found!")
        else:
            book = session.get(Book, orders.book_id)
            if not book:
                raise HTTPException(status_code=404, detail=f"Book with ID {orders.book_id} not found!")
    
    return place_orders_in_db(orders)


@app.get("/orders/", response_model=list[Order])
def get_orders():
    return get_orders_from_db()

@app.post("/chat/")
def chat_with_data(prompt: str):
    res = client.chat.completions.create(
        model = "gpt-4o-mini",
        response_model = AiAction,
        messages = [{"role": "user", "content": prompt}]
    )

    action = res.action.lower()

    if action == "add_book" and res.books:
        return add_books(res.books)
    elif action == "place_order" and res.orders:
        return place_orders(res.orders)
    else:
        raise HTTPException(status_code=400, detail="Unknown action!")


if __name__ == "__main__":
    time.sleep(2)
    SQLModel.metadata.create_all(engine)
    uvicorn.run(app, host="0.0.0.0", port=80)


# curl -X 'POST' 'http://localhost:4000/books/' -H 'Content-Type: application/json' -d '{
#   "title": "HappyLooop",
#   "price": 500,
#   "author": "0m@r"
# }'
#
# curl -X 'GET' 'http://localhost:4000/books/'
#
# curl -X 'POST' 'http://localhost:4000/orders/' -H 'Content-Type: application/json' -d '{
#   "book_id": 1,
#   "customer_name": "Astro",
#   "customer_contact": "astro@astro.com",
#   "status": "pending"
# }'
