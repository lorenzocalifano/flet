import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
SessionLocal = None
engine = None

try:
    # Percorso assoluto della directory del file corrente (funziona anche per eseguibili PyInstaller)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Percorso completo del database nella stessa cartella (o accanto all'eseguibile)
    DB_PATH = os.path.join(BASE_DIR, "..", "gestionale_magazzino.db")

    # Creazione engine SQLite
    engine = create_engine(
        f"sqlite:///{os.path.abspath(DB_PATH)}",
        connect_args={"check_same_thread": False}
    )

    # Creazione sessione
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    print(f"Database collegato correttamente: {os.path.abspath(DB_PATH)}")

except Exception as e:
    print(f"Errore durante la connessione al database: {e}")
    # Qui potresti anche implementare un fallback o terminare l'applicazione in modo controllato