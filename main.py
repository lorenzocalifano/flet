import os
import subprocess
import flet as ft

# Percorso standard per il database su macOS
BASE_DIR = os.path.expanduser("~/Library/Application Support/Gestionale_Magazzino")
DB_PATH = os.path.join(BASE_DIR, "gestionale_magazzino.db")

# Crea la cartella se non esiste
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR, exist_ok=True)

# Passa il percorso al database.py
os.environ["DB_PATH"] = DB_PATH
print(f"Database collegato correttamente: {DB_PATH}")

# Import Delle Pagine
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
from app.pages.rental_edit_page import rental_edit_page
from populate_database import populate

# Database e Modelli
from app.models.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.product import Product

# Controllo iniziale database
Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    if db.query(User).count() == 0 and db.query(Product).count() == 0:
        print("Primo avvio: popolamento database con dati fake...")
        populate()
    else:
        print("Database già popolato, nessuna modifica.")
finally:
    db.close()

# noinspection PyUnreachableCode
def main(page: ft.Page):
    # Impostazioni grafiche globali
    page.title = "Gestionale Magazzino"
    page.theme_mode = "light"
    page.theme = ft.Theme(font_family="Montserrat")
    page.window_maximized = True
    page.window_full_screen = False
    page.update()

    # Routing con controllo autenticazione
    def route_change(e):
        page.views.clear()

        protected_routes = [
            "/dashboard", "/catalog", "/history", "/user_management",
            "/damage_report", "/notifications", "/rental_sale",
            "/add_edit_product", "/product_detail", "/quantity_update",
            "/notification_detail"
        ]

        # Controllo autenticazione corretto
        user_name = page.session.get("user_name")
        user_role = page.session.get("user_role")
        if any(page.route.startswith(r) for r in protected_routes):
            if not user_name or not user_role or user_name == "Utente" or user_role == "N/A":
                page.go("/")
                return

        # Routing normale
        if page.route.startswith("/product_detail"):
            page.views.append(product_detail_page(page))
        elif page.route.startswith("/quantity_update"):
            page.views.append(quantity_update_page(page))
        elif page.route.startswith("/notification_detail"):
            page.views.append(notification_detail_page(page))
        elif page.route.startswith("/add_edit_product"):
            page.views.append(add_edit_product_page(page))
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
        elif page.route.startswith("/rental_edit"):
            page.views.append(rental_edit_page(page))
        elif page.route == "/reset_password":
            page.views.append(reset_password_page(page))

        page.update()

    page.on_route_change = route_change
    page.go(page.route or "/")

# Avvio applicazione
if os.getenv("DOCKER") == "1":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550, host="0.0.0.0")
else:
    ft.app(target=main, view=ft.AppView.FLET_APP)