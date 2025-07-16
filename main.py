import sys
import os

sys.path.append(os.path.dirname(__file__))

#Entry point dell'app Flet
from app.models.database import Base, engine
from app.models import user, product, rental, sale, damage, notification

# Crea tutte le tabelle (solo la prima volta)
Base.metadata.create_all(bind=engine)

print("Database creato con successo!")