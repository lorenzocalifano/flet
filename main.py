import flet as ft

# === IMPORT DELLE PAGINE ===
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

# === DATABASE E MODELLI ===
from app.models.database import Base, engine, SessionLocal
from app.models.user import User
from app.models import *

# === SERVICES E SCHEMAS ===
from app.services.auth_service import register_user
from app.schemas.user_schema import UserCreate, UserRole

# === AVVIO APPLICAZIONE ===
def main(page: ft.Page):
    # Impostazioni grafiche globali
    page.title = "Gestionale Magazzino"
    page.theme_mode = "light"
    page.theme = ft.Theme(font_family="Montserrat")

    # Proviamo a massimizzare sempre la finestra all'avvio
    page.window_maximized = True
    page.window_full_screen = False  # lasciamo solo massimizzata, non fullscreen
    page.update()

    # === CREAZIONE DB E UTENTI DI TEST ===
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).first():
            register_user(db, UserCreate(
                nome="Mario", cognome="Rossi",
                email="mario.rossi@test.com", password="123456",
                ruolo=UserRole.RESPONSABILE
            ))
            register_user(db, UserCreate(
                nome="Luca", cognome="Bianchi",
                email="luca.bianchi@test.com", password="123456",
                ruolo=UserRole.SEGRETERIA
            ))
            register_user(db, UserCreate(
                nome="Giulia", cognome="Verdi",
                email="giulia.verdi@test.com", password="123456",
                ruolo=UserRole.MAGAZZINIERE
            ))
            print("✅ Utenti di test creati!")
    finally:
        db.close()

    # === GESTIONE ROUTING ===
    # noinspection PyUnreachableCode

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

    page.on_route_change = route_change
    page.go(page.route or "/")

# === AVVIO APP ===
ft.app(target=main)