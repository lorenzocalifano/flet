import flet as ft
from datetime import date
from app.models.database import SessionLocal
from app.services.product_service import get_all_products, update_product_quantity
from app.services.rental_service import create_rental, conclude_rental, get_rental_by_id
from app.services.sale_service import create_sale, get_sale_by_id
from app.services.notification_service import create_notification
from app.schemas.rental_schema import RentalCreate
from app.schemas.sale_schema import SaleCreate
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header

def rental_sale_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    if page.session.get("user_role") not in ["RESPONSABILE", "SEGRETERIA"]:
        return ft.View(
            route="/rental_sale",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text(
                            "Utente non autorizzato",
                            size=22,
                            color=ft.Colors.RED,
                            weight=ft.FontWeight.BOLD
                        ),
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        alignment=ft.alignment.center
                    )
                ], expand=True)
            ]
        )

    db = SessionLocal()
    prodotti = get_all_products(db)
    db.close()

    product_options = [ft.dropdown.Option(f"{p.id} - {p.nome}") for p in prodotti]

    prodotto_dropdown = ft.Dropdown(label="Prodotto", options=product_options, width=300)
    quantita_field = ft.TextField(label="Quantità", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    cliente_field = ft.TextField(label="Cliente", width=300)
    data_fine_field = ft.TextField(label="Data Fine (solo noleggi, YYYY-MM-DD)", width=300)
    metodo_dropdown = ft.Dropdown(
        label="Metodo di Pagamento",
        options=[ft.dropdown.Option(m) for m in ["contanti", "paypal", "carta di credito"]],
        width=200
    )
    message_text = ft.Text("", size=16)

    def handle_rental(e):
        if not all([prodotto_dropdown.value, quantita_field.value, cliente_field.value, data_fine_field.value, metodo_dropdown.value]):
            message_text.value = "Compila tutti i campi per il noleggio!"
            message_text.color = "red"
            page.update()
            return

        prodotto_id = int(prodotto_dropdown.value.split(" - ")[0])
        db = SessionLocal()
        try:
            nuovo_noleggio = create_rental(db, RentalCreate(
                prodotto_id=prodotto_id,
                quantita=int(quantita_field.value),
                cliente=cliente_field.value,
                data_inizio=date.today(),
                data_fine=date.fromisoformat(data_fine_field.value),
                stato="in corso",
                metodo_pagamento=metodo_dropdown.value
            ))
            create_notification(db, f"Noleggio registrato per {cliente_field.value}", "noleggio", nuovo_noleggio.id)
            message_text.value = "Noleggio registrato con successo!"
            message_text.color = "green"
        except Exception as ex:
            message_text.value = f"Errore: {str(ex)}"
            message_text.color = "red"
        finally:
            db.close()
        page.update()

    def handle_sale(e):
        if not all([prodotto_dropdown.value, quantita_field.value, cliente_field.value, metodo_dropdown.value]):
            message_text.value = "Compila tutti i campi per la vendita!"
            message_text.color = "red"
            page.update()
            return

        prodotto_id = int(prodotto_dropdown.value.split(" - ")[0])
        db = SessionLocal()
        try:
            nuova_vendita = create_sale(db, SaleCreate(
                prodotto_id=prodotto_id,
                quantita=int(quantita_field.value),
                cliente=cliente_field.value,
                data_vendita=date.today(),
                stato="confermato",
                metodo_pagamento=metodo_dropdown.value
            ))
            create_notification(db, f"Vendita registrata per {cliente_field.value}", "vendita", nuova_vendita.id)
            message_text.value = "Vendita registrata con successo!"
            message_text.color = "green"
        except Exception as ex:
            message_text.value = f"Errore: {str(ex)}"
            message_text.color = "red"
        finally:
            db.close()
        page.update()

    content = ft.Column([
        build_header(page, "Noleggi e Vendite"),
        prodotto_dropdown,
        quantita_field,
        cliente_field,
        data_fine_field,
        metodo_dropdown,
        ft.Row([
            ft.ElevatedButton("Registra Noleggio", on_click=handle_rental),
            ft.ElevatedButton("Registra Vendita", on_click=handle_sale)
        ], spacing=10),
        message_text
    ], spacing=15)

    return ft.View(
        route="/rental_sale",
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