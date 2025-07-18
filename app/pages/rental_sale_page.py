import flet as ft
from datetime import date
from app.models.database import SessionLocal
from app.services.product_service import get_all_products, update_product_quantity
from app.services.rental_service import create_rental
from app.services.sale_service import create_sale
from app.services.notification_service import create_notification
from app.schemas.rental_schema import RentalCreate
from app.schemas.sale_schema import SaleCreate
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header

def rental_sale_page(page: ft.Page):
    # Controllo Autenticazione Utente
    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route="/rental_sale",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text(
                            "Utente Non Autorizzato",
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

    # Impostazioni Tema
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # Recupero Prodotti Dal Database
    db = SessionLocal()
    prodotti = get_all_products(db)
    db.close()

    # Dropdown Prodotti E Campi Di Inserimento
    product_dropdown = ft.Dropdown(
        label="Prodotto",
        options=[ft.dropdown.Option(f"{p.id} - {p.nome}") for p in prodotti],
        width=300
    )
    quantita_field = ft.TextField(label="Quantità", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    cliente_field = ft.TextField(label="Cliente", width=300)
    data_fine_field = ft.TextField(label="Data Fine (solo per noleggi, formato YYYY-MM-DD)", width=300)
    metodo_pagamento_dropdown = ft.Dropdown(
        label="Metodo Pagamento",
        options=[
            ft.dropdown.Option("Contanti"),
            ft.dropdown.Option("Carta di Credito"),
            ft.dropdown.Option("PayPal")
        ],
        width=300
    )
    message_text = ft.Text("", size=16, color="green")

    # Funzione Per Gestire Noleggi
    def handle_rental(e):
        if not product_dropdown.value or not quantita_field.value or not cliente_field.value or not data_fine_field.value or not metodo_pagamento_dropdown.value:
            message_text.value = "Tutti i campi sono obbligatori per i noleggi!"
            message_text.color = "red"
            page.update()
            return

        prodotto_id = int(product_dropdown.value.split(" - ")[0])
        try:
            data_fine = date.fromisoformat(data_fine_field.value)
        except ValueError:
            message_text.value = "Formato data non valido (usa YYYY-MM-DD)"
            message_text.color = "red"
            page.update()
            return

        db = SessionLocal()
        try:
            rental = create_rental(db, RentalCreate(
                prodotto_id=prodotto_id,
                quantita=int(quantita_field.value),
                cliente=cliente_field.value,
                data_inizio=date.today(),
                data_fine=data_fine,
                stato="in corso",
                metodo_pagamento=metodo_pagamento_dropdown.value
            ))
            update_product_quantity(db, prodotto_id, -int(quantita_field.value))
            create_notification(
                db,
                messaggio=f"Noleggio registrato per {cliente_field.value} - Prodotto ID {prodotto_id}",
                tipo="noleggio",
                operazione_id=rental.id
            )
            message_text.value = "Noleggio registrato correttamente!"
            message_text.color = "green"
            page.go("/notifications")
        except Exception as ex:
            message_text.value = f"Errore durante il noleggio: {str(ex)}"
            message_text.color = "red"
        finally:
            db.close()
        page.update()

    # Funzione Per Gestire Vendite
    def handle_sale(e):
        if not product_dropdown.value or not quantita_field.value or not cliente_field.value or not metodo_pagamento_dropdown.value:
            message_text.value = "Tutti i campi sono obbligatori per le vendite!"
            message_text.color = "red"
            page.update()
            return

        prodotto_id = int(product_dropdown.value.split(" - ")[0])

        db = SessionLocal()
        try:
            sale = create_sale(db, SaleCreate(
                prodotto_id=prodotto_id,
                quantita=int(quantita_field.value),
                cliente=cliente_field.value,
                data_vendita=date.today(),
                stato="confermato",
                metodo_pagamento=metodo_pagamento_dropdown.value
            ))
            update_product_quantity(db, prodotto_id, -int(quantita_field.value))
            create_notification(
                db,
                messaggio=f"Vendita registrata per {cliente_field.value} - Prodotto ID {prodotto_id}",
                tipo="vendita",
                operazione_id=sale.id
            )
            message_text.value = "Vendita registrata correttamente!"
            message_text.color = "green"
            page.go("/notifications")
        except Exception as ex:
            message_text.value = f"Errore durante la vendita: {str(ex)}"
            message_text.color = "red"
        finally:
            db.close()
        page.update()

    # Composizione Contenuto Pagina
    content = ft.Column([
        build_header(page, "Registra Noleggi E Vendite"),
        product_dropdown,
        quantita_field,
        cliente_field,
        data_fine_field,
        metodo_pagamento_dropdown,
        ft.Row([
            ft.ElevatedButton("Registra Noleggio", on_click=handle_rental, width=200),
            ft.ElevatedButton("Registra Vendita", on_click=handle_sale, width=200)
        ], spacing=20),
        message_text
    ], spacing=15, expand=True)

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