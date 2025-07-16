import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import get_all_products
from app.services.damage_service import report_damage
from app.schemas.damage_schema import DamageCreate
from datetime import date

def damage_report_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    if page.session.get("user_role") not in ["RESPONSABILE", "MAGAZZINIERE"]:
        page.go("/dashboard")
        return

    db = SessionLocal()
    prodotti = get_all_products(db)
    db.close()

    product_options = [ft.dropdown.Option(f"{p.id} - {p.nome}") for p in prodotti]
    prodotto_dropdown = ft.Dropdown(options=product_options, width=300)
    descrizione_field = ft.TextField(label="Descrizione del danno", multiline=True, width=300)
    message_text = ft.Text("", size=16, color="green")

    def handle_report(e):
        if not prodotto_dropdown.value:
            message_text.value = "Seleziona un prodotto."
            message_text.color = "red"
            page.update()
            return
        prodotto_id = int(prodotto_dropdown.value.split(" - ")[0])
        db = SessionLocal()
        report_damage(db, DamageCreate(
            prodotto_id=prodotto_id,
            descrizione=descrizione_field.value,
            data_segnalazione=date.today()
        ))
        db.close()
        message_text.value = "✅ Danno segnalato!"
        message_text.color = "green"
        page.update()

    menu_items = [
        ft.ElevatedButton("Dashboard", on_click=lambda e: page.go("/dashboard")),
        ft.ElevatedButton("Catalogo", on_click=lambda e: page.go("/catalog")),
        ft.ElevatedButton("Danni", on_click=lambda e: page.go("/damage_report")),
        ft.ElevatedButton("Notifiche", on_click=lambda e: page.go("/notifications"))
    ]

    content = ft.Column([
        ft.Text("Segnalazione Danni", size=30, weight=ft.FontWeight.BOLD),
        prodotto_dropdown, descrizione_field,
        ft.ElevatedButton("Segnala Danno", on_click=handle_report, width=250),
        message_text
    ], spacing=10)

    return ft.View(
        route="/damage_report",
        bgcolor="#1e90ff",
        controls=[
            ft.Row([
                ft.Container(content=ft.Column(menu_items, spacing=10), width=220, bgcolor=ft.colors.BLUE_700, padding=15),
                ft.Container(content=content, expand=True, bgcolor=ft.colors.WHITE, padding=30, border_radius=15,
                             shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=ft.colors.with_opacity(0.25, ft.colors.BLACK)))
            ], expand=True)
        ]
    )