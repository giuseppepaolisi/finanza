import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
print(f"DEBUG: Password: '{DB_PASSWORD}' - Lunghezza: {len(DB_PASSWORD) if DB_PASSWORD else 0}")

# Costruzione URL
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
# factory per creare nuove sessioni di connessione al database 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def init_db():
    # Chiamato una volta all'avvio dell'app
    Base.metadata.create_all(bind=engine)
    
def get_db():
    # Dipendenza per ottenere una sessione di database per ogni richiesta
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()