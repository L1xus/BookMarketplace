from sqlmodel import create_engine

POSTGRES_USER = "astro"
POSTGRES_PASSWORD = "astro"
POSTGRES_HOST = "postgres"
POSTGRES_PORT = 5432
POSTGRES_DB = "books_marketplace"

postgres_url = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(postgres_url, echo=True)
