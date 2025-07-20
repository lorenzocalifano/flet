import random
from datetime import datetime, timedelta, date
from faker import Faker
from sqlalchemy import text
from app.models.database import SessionLocal, Base, engine
from app.services.auth_service import register_user
from app.schemas.user_schema import UserCreate, UserRole
from app.services.product_service import create_product
from app.services.rental_service import create_rental
from app.services.sale_service import create_sale
from app.services.damage_service import report_damage
from app.services.notification_service import create_notification
from app.schemas.product_schema import ProductCreate
from app.schemas.rental_schema import RentalCreate
from app.schemas.sale_schema import SaleCreate
from app.schemas.damage_schema import DamageCreate

fake = Faker("it_IT")

def populate():
    """Popola il database con dati fittizi per i test"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("Pulizia database...")
    db.execute(text("DELETE FROM notifications"))
    db.execute(text("DELETE FROM damages"))
    db.execute(text("DELETE FROM rentals"))
    db.execute(text("DELETE FROM sales"))
    db.execute(text("DELETE FROM products"))
    db.execute(text("DELETE FROM users"))
    db.commit()

    print("Creazione utenti di test...")
    ruoli = [UserRole.RESPONSABILE, UserRole.SEGRETERIA, UserRole.MAGAZZINIERE]
    for i in range(20):
        ruolo = random.choice(ruoli)
        email = fake.unique.email()
        register_user(
            db,
            UserCreate(
                nome=fake.first_name(),
                cognome=fake.last_name(),
                email=email,
                password="123456",
                ruolo=ruolo
            )
        )
        print(f"{ruolo.value.upper()} -> {email} / 123456")

    print("Creazione prodotti...")
    categorie = ["Audio", "Luci", "Video", "Strumenti Musicali", "Accessori"]
    modelli = ["Pro", "Max", "Lite", "X-Series", "MK2"]
    dimensioni = ["Piccolo", "Medio", "Grande"]
    brands = ["Yamaha", "Sony", "Behringer", "JBL", "Roland"]

    prodotti_creati = []
    tentativi = 0
    while len(prodotti_creati) < 50 and tentativi < 100:
        tentativi += 1
        try:
            p = create_product(db, ProductCreate(
                nome=fake.unique.word().capitalize(),  # unique per ridurre collisioni
                categoria=random.choice(categorie),
                quantita=random.randint(5, 30),
                modello=random.choice(modelli),
                dimensione=random.choice(dimensioni),
                brand=random.choice(brands),
                potenza=random.randint(50, 2000)
            ))
            prodotti_creati.append(p)
        except ValueError as e:
            # Nome duplicato, rigenera
            continue

    print("Creazione noleggi...")
    mese_corrente = datetime.now().month
    for i in range(30):
        prodotto = random.choice(prodotti_creati)
        quantita = random.randint(1, min(5, prodotto.quantita))

        # 50% dei noleggi nel mese corrente
        if i < 15:
            start_date = date(datetime.now().year, mese_corrente, random.randint(1, min(28, datetime.now().day)))
        else:
            start_date = fake.date_this_year()

        end_date = start_date + timedelta(days=random.randint(1, 10))
        cliente = fake.name()
        metodo = random.choice(["contanti", "paypal", "carta di credito"])

        create_rental(db, RentalCreate(
            prodotto_id=prodotto.id,
            quantita=quantita,
            cliente=cliente,
            data_inizio=start_date,
            data_fine=end_date,
            stato=random.choice(["in corso", "concluso"]),
            metodo_pagamento=metodo
        ))

    print("Creazione vendite...")
    for _ in range(20):
        prodotto = random.choice(prodotti_creati)

        # Calcola disponibilità reale del prodotto
        danneggiati = random.randint(0, min(2, prodotto.quantita))  # simulazione danni eventuali
        disponibili = max(0, prodotto.quantita - danneggiati)

        if disponibili <= 0:
            continue  # salta questo prodotto se non ci sono pezzi disponibili

        quantita = random.randint(1, disponibili)
        cliente = fake.name()
        metodo = random.choice(["contanti", "paypal", "carta di credito"])

        try:
            create_sale(db, SaleCreate(
                prodotto_id=prodotto.id,
                quantita=quantita,
                cliente=cliente,
                data_vendita=fake.date_this_year(),
                stato=random.choice(["confermato", "annullato"]),
                metodo_pagamento=metodo
            ))
        except Exception as e:
            print(f"Errore nella creazione vendita per {prodotto.nome}: {e}")

    print("Segnalazione danni...")
    for _ in range(10):
        prodotto = random.choice(prodotti_creati)
        report_damage(db, DamageCreate(
            prodotto_id=prodotto.id,
            descrizione=fake.sentence(nb_words=6),
            data_segnalazione=datetime.now().date()
        ))

    print("Creazione notifiche manuali...")
    for _ in range(10):
        create_notification(
            db,
            messaggio=fake.sentence(nb_words=8),
            tipo=random.choice(["generale", "avviso"]),
            operazione_id=random.choice(prodotti_creati).id
        )

    db.close()
    print("Database popolato con successo!")

if __name__ == "__main__":
    populate()