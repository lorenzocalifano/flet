import flet as ft
from datetime import date
from app.models.database import SessionLocal
from app.services.product_service import get_all_products
from app.services.damage_service import report_damage
from app.schemas.damage_schema import DamageCreate
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header

def damage_report_page(page: ft.Page):
    # Controllo Autenticazione Utente
    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route="/damage_report",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text("Utente Non Autorizzato", size=22, color=ft.Colors.RED, weight=ft.FontWeight.BOLD),
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        alignment=ft.alignment.center
                    )
                ], expand=True)
            ]
        )

    # Impostazioni Tema
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # Recupero Prodotti Dal Database
    db = SessionLocal()
    prodotti = get_all_products(db)
    db.close()

    product_dropdown = ft.Dropdown(
        label="Prodotto",
        options=[ft.dropdown.Option(f"{p.id} - {p.nome}") for p in prodotti],
        width=300
    )
    descrizione_field = ft.TextField(label="Descrizione Del Danno", multiline=True, width=300)
    message_text = ft.Text("", size=16, color="green")

    def handle_report(e):
        if not product_dropdown.value or not descrizione_field.value:
            message_text.value = "Tutti i campi sono obbligatori"
            message_text.color = "red"
            page.update()
            return

        prodotto_id = int(product_dropdown.value.split(" - ")[0])

        db = SessionLocal()
        try:
            report_damage(db, DamageCreate(
                prodotto_id=prodotto_id,
                descrizione=descrizione_field.value,
                data_segnalazione=date.today()
            ))
            message_text.value = "Danno segnalato correttamente"
            message_text.color = "green"
        except Exception as ex:
            message_text.value = f"Errore: {str(ex)}"
            message_text.color = "red"
        finally:
            db.close()
        page.update()

    content = ft.Column([
        build_header(page, "Segnalazione Danni"),
        product_dropdown,
        descrizione_field,
        ft.ElevatedButton("Segnala Danno", on_click=handle_report, width=250),
        message_text
    ], spacing=15, expand=True)

    return ft.View(
        route="/damage_report",
        bgcolor="#f5f5f5",
        controls=[
            ft.Row([
                build_menu(page),
                ft.Container(
                    content=content,
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    padding=30,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK)
                    )
                )
            ], expand=True)
        ]
    )