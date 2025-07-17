import random
from datetime import date, timedelta
from app.models.database import Base, engine, SessionLocal
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserRole
from app.services.auth_service import register_user
from app.services.product_service import create_product
from app.schemas.product_schema import ProductCreate
from app.services.rental_service import create_rental
from app.schemas.rental_schema import RentalCreate
from app.services.sale_service import create_sale
from app.schemas.sale_schema import SaleCreate
from app.services.damage_service import report_damage
from app.schemas.damage_schema import DamageCreate
from app.services.notification_service import create_notification

# ✅ Ricrea il database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ✅ 1. Utenti di test
nomi = [
    ("Mario", "Rossi", "RESPONSABILE"),
    ("Luca", "Bianchi", "SEGRETERIA"),
    ("Giulia", "Verdi", "MAGAZZINIERE"),
    ("Paolo", "Neri", "MAGAZZINIERE"),
    ("Sara", "Blu", "SEGRETERIA"),
]
for nome, cognome, ruolo in nomi:
    register_user(
        db,
        UserCreate(
            nome=nome,
            cognome=cognome,
            email=f"{nome.lower()}.{cognome.lower()}@test.com",
            password="123456",
            ruolo=UserRole[ruolo]
        )
    )

# ✅ 2. Prodotti
categorie = ["Audio", "Video", "Luci", "Accessori"]
prodotti = []
for i in range(30):
    p = create_product(
        db,
        ProductCreate(
            nome=f"Prodotto {i+1}",
            categoria=random.choice(categorie),
            quantita=random.randint(5, 30)
        )
    )
    prodotti.append(p)

# ✅ 3. Noleggi e Vendite
metodi_pagamento = ["contanti", "carta di credito", "paypal"]
clienti = ["Lorenzo", "Andrea", "Chiara", "Francesca", "Matteo", "Elisa"]

for _ in range(100):  # 100 noleggi
    prodotto = random.choice(prodotti)
    quantita = random.randint(1, min(3, prodotto.quantita))
    data_inizio = date.today() - timedelta(days=random.randint(1, 60))
    data_fine = data_inizio + timedelta(days=random.randint(1, 10))
    create_rental(
        db,
        RentalCreate(
            prodotto_id=prodotto.id,
            quantita=quantita,
            cliente=random.choice(clienti),
            data_inizio=data_inizio,
            data_fine=data_fine,
            stato=random.choice(["in corso", "concluso"]),
            metodo_pagamento=random.choice(metodi_pagamento)
        )
    )

for _ in range(80):  # 80 vendite
    prodotto = random.choice(prodotti)
    quantita = random.randint(1, min(2, prodotto.quantita))
    create_sale(
        db,
        SaleCreate(
            prodotto_id=prodotto.id,
            quantita=quantita,
            cliente=random.choice(clienti),
            data_vendita=date.today() - timedelta(days=random.randint(1, 60)),
            stato=random.choice(["confermato", "annullato"]),
            metodo_pagamento=random.choice(metodi_pagamento)
        )
    )

# ✅ 4. Danni
for _ in range(40):
    prodotto = random.choice(prodotti)
    report_damage(
        db,
        DamageCreate(
            prodotto_id=prodotto.id,
            descrizione=f"Danno su {prodotto.nome} - urto durante trasporto",
            data_segnalazione=date.today() - timedelta(days=random.randint(1, 30))
        )
    )

# ✅ 5. Notifiche
for _ in range(50):
    create_notification(
        db,
        messaggio=f"Notifica automatica: {random.choice(['controllo magazzino', 'scadenza noleggio', 'nuovo ordine'])}",
        tipo=random.choice(["noleggio", "vendita", "altro"]),
        operazione_id=random.randint(1, 50)
    )

db.close()
print("✅ Database popolato con successo!")