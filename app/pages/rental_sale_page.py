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
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    if page.session.get("user_role") not in ["RESPONSABILE", "SEGRETERIA"]:
        page.go("/dashboard")
        return

    db = SessionLocal()
    prodotti = get_all_products(db)
    db.close()

    prodotto_dropdown = ft.Dropdown(
        label="Prodotto",
        options=[ft.dropdown.Option(str(p.id), f"{p.nome} ({p.categoria})") for p in prodotti],
        width=300
    )
    tipo_operazione = ft.Dropdown(
        label="Operazione",
        options=[ft.dropdown.Option("Noleggio"), ft.dropdown.Option("Vendita")],
        width=300
    )
    quantita_field = ft.TextField(label="Quantità", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    cliente_field = ft.TextField(label="Cliente", width=300)
    metodo_pagamento = ft.Dropdown(
        label="Metodo pagamento",
        options=[
            ft.dropdown.Option("contanti"),
            ft.dropdown.Option("paypal"),
            ft.dropdown.Option("carta di credito")
        ],
        width=300
    )
    data_inizio = ft.TextField(label="Data inizio (YYYY-MM-DD)", value=str(date.today()), width=300)
    data_fine = ft.TextField(label="Data fine (solo per noleggi)", width=300)
    message_text = ft.Text("", size=16)

    def handle_submit(e):
        if not prodotto_dropdown.value or not tipo_operazione.value or not quantita_field.value \
                or not cliente_field.value or not metodo_pagamento.value:
            message_text.value = "⚠️ Tutti i campi sono obbligatori!"
            message_text.color = "red"
            page.update()
            return

        if tipo_operazione.value == "Noleggio" and not data_fine.value:
            message_text.value = "⚠️ Per i noleggi devi inserire la data di fine!"
            message_text.color = "red"
            page.update()
            return

        db = SessionLocal()
        try:
            prodotto_id = int(prodotto_dropdown.value)
            quantita = int(quantita_field.value)

            if tipo_operazione.value == "Noleggio":
                create_rental(db, RentalCreate(
                    prodotto_id=prodotto_id,
                    quantita=quantita,
                    cliente=cliente_field.value,
                    data_inizio=date.fromisoformat(data_inizio.value),
                    data_fine=date.fromisoformat(data_fine.value),
                    stato="in corso",
                    metodo_pagamento=metodo_pagamento.value
                ))

                # ✅ Notifica per noleggio
                create_notification(
                    db,
                    messaggio=f"Noleggio registrato: {cliente_field.value} ha noleggiato {quantita}x Prodotto ID {prodotto_id} "
                              f"({data_inizio.value} → {data_fine.value})",
                    tipo="noleggio",
                    operazione_id=prodotto_id
                )

            else:
                create_sale(db, SaleCreate(
                    prodotto_id=prodotto_id,
                    quantita=quantita,
                    cliente=cliente_field.value,
                    data_vendita=date.fromisoformat(data_inizio.value),
                    stato="concluso",
                    metodo_pagamento=metodo_pagamento.value
                ))

                # ✅ Notifica per vendita
                create_notification(
                    db,
                    messaggio=f"Vendita registrata: {cliente_field.value} ha acquistato {quantita}x Prodotto ID {prodotto_id} "
                              f"({metodo_pagamento.value})",
                    tipo="vendita",
                    operazione_id=prodotto_id
                )

            update_product_quantity(db, prodotto_id, -quantita)
            message_text.value = f"✅ {tipo_operazione.value} registrato con successo!"
            message_text.color = "green"

            # ✅ PORTA DIRETTAMENTE ALLE NOTIFICHE
            page.go("/notifications")

        except Exception as ex:
            message_text.value = f"❌ Errore: {str(ex)}"
            message_text.color = "red"
        finally:
            db.close()
        page.update()

    content = ft.Column([
        build_header(page, "Registra Noleggio / Vendita"),
        tipo_operazione,
        prodotto_dropdown,
        quantita_field,
        cliente_field,
        metodo_pagamento,
        data_inizio,
        data_fine,
        ft.ElevatedButton("Registra", on_click=handle_submit, width=250),
        message_text
    ], spacing=15, expand=True)

    return ft.View(
        route="/rental_sale",
        bgcolor="#f9f9f9",
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