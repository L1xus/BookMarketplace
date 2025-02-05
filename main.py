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
from models import Book, ChatRequest, Order, AiAction
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = instructor.from_groq(Groq(api_key=GROQ_API_KEY))

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
def chat_with_data(req: ChatRequest):
    prompt = req.prompt

    res = client.chat.completions.create(
        model="llama3-70b-8192",
        response_model=AiAction,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI assistant that processes book orders.\n"
                    "You must always return structured JSON data following the AiAction schema.\n"
                    "Your action must always be 'add_book' or 'place_order'.\n\n"
                    "When generating books, follow this structure:\n"
                    "- title: str (required)\n"
                    "- price: float (required)\n"
                    "- author: str (required)\n"
                    "- pages: Optional[int] (optional)\n\n"
                    "When generating orders, follow this structure:\n"
                    "- book_id: int (required, must reference an existing book ID)\n"
                    "- customer_name: str (required)\n"
                    "- customer_contact: str (required)\n"
                    "- status: str (default='pending')\n\n"
                    "If the user wants to add books, generate books under 'books'.\n"
                    "If the user wants to place an order, generate orders under 'orders'."
                ),
            },
            {"role": "user", "content": prompt},
        ]
    )

    print(f"HERE IS THE RES: {res}")
    action = res.action.lower()
    print(f"HERE IS THE ACTION: {action}")

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
#
# curl -X 'POST' 'http://localhost:4000/chat/' -H 'Content-Type: application/json' -d '{
#   "prompt": "create 3 random orders"
# }'
