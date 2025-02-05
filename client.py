from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import Client
from database import engine
from typing import List

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)

@router.post("/", response_model=Client)
def create_client(client: Client):
    with Session(engine) as session:
        # Check if email already exists
        existing_client = session.exec(
            select(Client).where(Client.email == client.email)
        ).first()
        if existing_client:
            raise HTTPException(
                status_code=400,
                detail="A client with this email already exists"
            )
        
        # Create new client
        db_client = Client.from_orm(client)
        session.add(db_client)
        session.commit()
        session.refresh(db_client)
        return db_client

@router.get("/", response_model=List[Client])
def get_clients():
    with Session(engine) as session:
        clients = session.exec(select(Client)).all()
        return clients

@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int):
    with Session(engine) as session:
        client = session.get(Client, client_id)
        if not client:
            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )
        return client

@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, client_update: Client):
    with Session(engine) as session:
        db_client = session.get(Client, client_id)
        if not db_client:
            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )
        
        # Update client fields
        client_data = client_update.dict(exclude_unset=True)
        for key, value in client_data.items():
            if key != "id":  # Prevent updating the ID
                setattr(db_client, key, value)
        
        session.add(db_client)
        session.commit()
        session.refresh(db_client)
        return db_client

@router.delete("/{client_id}")
def delete_client(client_id: int):
    with Session(engine) as session:
        client = session.get(Client, client_id)
        if not client:
            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )
        
        session.delete(client)
        session.commit()
        return {"message": f"Client {client_id} deleted successfully"}

@router.get("/search/{email}", response_model=Client)
def search_client_by_email(email: str):
    with Session(engine) as session:
        client = session.exec(
            select(Client).where(Client.email == email)
        ).first()
        if not client:
            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )
        return client 