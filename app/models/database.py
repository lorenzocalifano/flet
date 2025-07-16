# Database connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database locale SQLite (file locale "app.db")
DATABASE_URL = "sqlite:///app.db"

# Crea il motore di connessione
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Sessione per interagire con il DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base per i modelli ORM
Base = declarative_base()

# Funzione di utilità per ottenere la sessione
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()