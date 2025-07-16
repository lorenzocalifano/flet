from app.models.database import Base, engine, SessionLocal
from app.models import *

from app.schemas.user_schema import UserCreate, UserRole
from app.services.auth_service import register_user, authenticate_user

from app.schemas.product_schema import ProductCreate
from app.services.product_service import create_product, get_all_products, update_quantity

from app.schemas.rental_schema import RentalCreate
from app.services.rental_service import create_rental, get_all_rentals, conclude_rental

from app.schemas.sale_schema import SaleCreate
from app.services.sale_service import create_sale, get_all_sales, cancel_sale

from app.schemas.damage_schema import DamageCreate
from app.services.damage_service import report_damage, get_all_damages

from app.services.notification_service import (
    create_notification, get_all_notifications, get_unread_notifications, mark_as_read
)

from datetime import date

# ✅ RESET DATABASE (solo in sviluppo)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("✅ Database creato con successo!")

db = SessionLocal()

# -------------------- TEST UTENTI --------------------
try:
    utente = register_user(
        db,
        UserCreate(
            nome="Mario",
            cognome="Rossi",
            email="mario.rossi@test.com",
            password="123456",
            ruolo=UserRole.SEGRETERIA
        )
    )
    print(f"✅ Utente creato: {utente.nome} {utente.cognome} ({utente.ruolo.value})")
except ValueError as e:
    print(f"⚠️ Registrazione fallita: {e}")

utente_login = authenticate_user(db, "mario.rossi@test.com", "123456")
if utente_login:
    print(f"✅ Login OK: {utente_login.nome} {utente_login.cognome}")
else:
    print("❌ Login fallito: credenziali errate")

# -------------------- TEST PRODOTTI --------------------
prodotto = create_product(
    db,
    ProductCreate(
        nome="Cassa Audio",
        categoria="Audio",
        brand="Yamaha",
        modello="DXR15",
        potenza="1100W",
        dimensione="15 pollici",
        quantita=5
    )
)
print(f"✅ Prodotto creato: {prodotto.nome} ({prodotto.quantita} disponibili)")

update_quantity(db, prodotto.id, 10)
print(f"✅ Quantità aggiornata: {prodotto.nome} (10 disponibili)")

print("📦 Catalogo prodotti:")
for p in get_all_products(db):
    print(f"- {p.nome} ({p.categoria}) - Quantità: {p.quantita}")

# -------------------- TEST NOLEGGI --------------------
noleggio = create_rental(
    db,
    RentalCreate(
        prodotto_id=prodotto.id,
        quantita=2,
        cliente="Luca Bianchi",
        data_inizio=date.today(),
        data_fine=date(2025, 7, 30)
    )
)
print(f"✅ Noleggio creato: {noleggio.cliente} ha noleggiato {noleggio.quantita}x {prodotto.nome}")

conclude_rental(db, noleggio.id)
print(f"✅ Noleggio concluso per {noleggio.cliente}")

print("📜 Storico noleggi:")
for n in get_all_rentals(db):
    print(f"- {n.cliente} | Prodotto ID {n.prodotto_id} | Stato: {n.stato}")

# -------------------- TEST VENDITE --------------------
vendita = create_sale(
    db,
    SaleCreate(
        prodotto_id=prodotto.id,
        quantita=1,
        cliente="Giulia Verdi",
        data_vendita=date.today()
    )
)
print(f"✅ Vendita registrata: {vendita.cliente} ha acquistato {vendita.quantita}x {prodotto.nome}")

cancel_sale(db, vendita.id)
print(f"✅ Vendita annullata per {vendita.cliente}")

print("📜 Storico vendite:")
for v in get_all_sales(db):
    print(f"- {v.cliente} | Prodotto ID {v.prodotto_id} | Stato: {v.stato}")

# -------------------- TEST DANNI --------------------
danno = report_damage(
    db,
    DamageCreate(
        prodotto_id=prodotto.id,
        descrizione="Cassa con graffi sulla scocca",
        data_segnalazione=date.today()
    )
)
print(f"✅ Danno segnalato: {danno.descrizione} per Prodotto ID {danno.prodotto_id}")

print("📜 Storico danni:")
for d in get_all_damages(db):
    print(f"- Prodotto ID {d.prodotto_id} | Descrizione: {d.descrizione} | Data: {d.data_segnalazione}")

# -------------------- TEST NOTIFICHE --------------------
create_notification(db, "Nuovo noleggio registrato")
create_notification(db, "Prodotto in esaurimento")
print("✅ Notifiche create manualmente")

print("🔔 Notifiche non lette:")
for n in get_unread_notifications(db):
    print(f"- {n.id}: {n.messaggio} | Letto: {n.letto}")

# Segna la prima come letta
prima_notifica = get_unread_notifications(db)[0]
mark_as_read(db, prima_notifica.id)
print(f"✅ Notifica {prima_notifica.id} segnata come letta")

print("📜 Storico notifiche:")
for n in get_all_notifications(db):
    print(f"- {n.id}: {n.messaggio} | Letto: {n.letto}")

db.close()