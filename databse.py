from sqlmodel import create_engine

POSTGRES_USER = "astro"
POSTGRES_PASSWORD = "astro"
POSTGRES_HOST = "postgres"
POSTGRES_PORT = 5432
POSTGRES_DB = "books_marketplace"

engine = create_engine(f"postgresql://{POSTGRES_USER}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
