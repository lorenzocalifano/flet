import os
import flet as ft

# Import Pagine
from app.pages.login_page import login_page
from app.pages.dashboard_page import dashboard_page
from app.pages.catalog_page import catalog_page
from app.pages.product_detail_page import product_detail_page
from app.pages.add_edit_product_page import add_edit_product_page
from app.pages.quantity_update_page import quantity_update_page
from app.pages.rental_sale_page import rental_sale_page
from app.pages.history_page import history_page
from app.pages.user_management_page import user_management_page
from app.pages.damage_report_page import damage_report_page
from app.pages.notifications_page import notifications_page
from app.pages.notification_detail_page import notification_detail_page
from app.pages.reset_password_page import reset_password_page

# Database e Modelli
from app.models.database import Base, engine, SessionLocal
from app.models.user import User
from app.models import *

# Servizi e Schemi
from app.services.auth_service import register_user
from app.schemas.user_schema import UserCreate, UserRole


# Funzione per creare un utente di test solo se non esiste già
def create_test_user_if_not_exists(db, nome, cognome, email, password, ruolo):
    # Crea un utente di test solo se non esiste già con quella email.
    if not db.query(User).filter(User.email == email).first():
        register_user(
            db,
            UserCreate(
                nome=nome,
                cognome=cognome,
                email=email,
                password=password,
                ruolo=ruolo
            )
        )
        print(f"Utente di test creato: {email}")


# main
def main(page: ft.Page):
    # Impostazioni grafiche globali
    page.title = "Gestionale Magazzino"
    page.theme_mode = "light"
    page.theme = ft.Theme(font_family="Montserrat")

    # Proviamo a massimizzare sempre la finestra all'avvio
    page.window_maximized = True
    page.window_full_screen = False  # lasciamo solo massimizzata, non fullscreen
    page.update()

    # Creazione DB e utenti di test ===
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        create_test_user_if_not_exists(db, "Lorenzo", "Califano", "s1114896@studenti.univpm.it", "123456", UserRole.RESPONSABILE)
        create_test_user_if_not_exists(db, "Chiara", "Carlomagno", "s1115047@studenti.univpm.it", "123456",UserRole.RESPONSABILE)
        create_test_user_if_not_exists(db, "Sabrina", "Ferretti", "s1115906@studenti.univpm.it", "123456",UserRole.RESPONSABILE)
        create_test_user_if_not_exists(db, "Mario", "Rossi", "mario.rossi@test.com", "123456", UserRole.RESPONSABILE)
        create_test_user_if_not_exists(db, "Luca", "Bianchi", "luca.bianchi@test.com", "123456", UserRole.SEGRETERIA)
        create_test_user_if_not_exists(db, "Giulia", "Verdi", "giulia.verdi@test.com", "123456", UserRole.MAGAZZINIERE)
    finally:
        db.close()

    # gestione route
    def route_change(e):
        # puliamo tutte le viste prima di caricare la nuova
        page.views.clear()

        # controlliamo la route e carichiamo la view corretta
        if page.route.startswith("/product_detail"):
            page.views.append(product_detail_page(page))
        elif page.route.startswith("/quantity_update"):
            page.views.append(quantity_update_page(page))
        elif page.route.startswith("/notification_detail"):
            page.views.append(notification_detail_page(page))
        elif page.route == "/":
            page.views.append(login_page(page))
        elif page.route == "/dashboard":
            page.views.append(dashboard_page(page))
        elif page.route == "/catalog":
            page.views.append(catalog_page(page))
        elif page.route == "/history":
            page.views.append(history_page(page))
        elif page.route == "/user_management":
            page.views.append(user_management_page(page))
        elif page.route == "/damage_report":
            page.views.append(damage_report_page(page))
        elif page.route == "/notifications":
            page.views.append(notifications_page(page))
        elif page.route == "/rental_sale":
            page.views.append(rental_sale_page(page))
        elif page.route == "/add_edit_product":
            page.views.append(add_edit_product_page(page))
        elif page.route == "/reset_password":
            page.views.append(reset_password_page(page))

        page.update()

    # Assegniamo la funzione di cambio route
    page.on_route_change = route_change
    page.go(page.route or "/")


# avvio app
if os.getenv("DOCKER") == "1":
    # Modalità Web per Docker (permette di usare da browser)
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        port=8550,
        host="0.0.0.0"
    )
else:
    # Modalità nativa per l'eseguibile e avvio manuale
    ft.app(
        target=main,
        view=ft.AppView.FLET_APP
    )