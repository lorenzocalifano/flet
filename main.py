import flet as ft

# ✅ Pagine
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

# ✅ Database e modelli
from app.models.database import Base, engine, SessionLocal
from app.models.user import User
from app.models import *

# ✅ Services e Schemas
from app.services.auth_service import register_user
from app.schemas.user_schema import UserCreate, UserRole
from datetime import date

def main(page: ft.Page):
    page.title = "Gestionale Magazzino"
    page.theme_mode = "light"

    # ✅ Login piccolo all'avvio
    page.window_maximized = False
    page.window_full_screen = False
    page.window_width = 420
    page.window_height = 520
    page.window_resizable = True
    page.window_bgcolor = ft.Colors.BLUE_700
    page.bgcolor = "#1e90ff"

    # ✅ Crea DB e utenti test
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).first():
            register_user(db, UserCreate(nome="Mario", cognome="Rossi",
                                         email="mario.rossi@test.com", password="123456",
                                         ruolo=UserRole.RESPONSABILE))
            register_user(db, UserCreate(nome="Luca", cognome="Bianchi",
                                         email="luca.bianchi@test.com", password="123456",
                                         ruolo=UserRole.SEGRETERIA))
            register_user(db, UserCreate(nome="Giulia", cognome="Verdi",
                                         email="giulia.verdi@test.com", password="123456",
                                         ruolo=UserRole.MAGAZZINIERE))
            print("✅ Utenti di test creati!")
    finally:
        db.close()

    # noinspection PyUnreachableCode

    # ✅ Routing
    def route_change(e):
        page.views.clear()

        # ✅ Se non siamo più nel login → massimizza
        if page.route != "/":
            page.window_maximized = True
            page.window_full_screen = False  # evita modalità "iPad" su Mac
            page.window_width = 1280
            page.window_height = 720

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
        elif page.route == "/reset_password":
            page.views.append(reset_password_page(page))

        page.update()

    page.on_route_change = route_change
    page.go(page.route or "/")


ft.app(target=main)