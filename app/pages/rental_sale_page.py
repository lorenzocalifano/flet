import flet as ft
from datetime import date
from app.models.database import SessionLocal
from app.services.product_service import get_all_products, update_quantity
from app.services.rental_service import create_rental
from app.services.sale_service import create_sale
from app.services.notification_service import create_notification
from app.services.damage_service import count_damages_for_product
from app.schemas.rental_schema import RentalCreate
from app.schemas.sale_schema import SaleCreate
from app.utils.menu_builder import build_menu

def rental_sale_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    if page.session.get("user_role") not in ["RESPONSABILE", "SEGRETERIA"]:
        page.go("/dashboard")
        return

    db = SessionLocal()
    prodotti = get_all_products(db)
    db.close()

    product_options = [ft.dropdown.Option(f"{p.id} - {p.nome}") for p in prodotti]

    tipo_operazione = ft.Dropdown(
        options=[ft.dropdown.Option("Noleggio"), ft.dropdown.Option("Vendita")],
        value="Noleggio", width=300
    )
    prodotto_dropdown = ft.Dropdown(options=product_options, width=300)
    quantita_field = ft.TextField(label="Quantità", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    cliente_field = ft.TextField(label="Cliente", width=300)
    metodo_pagamento = ft.Dropdown(
        options=[
            ft.dropdown.Option("contanti"),
            ft.dropdown.Option("carta di credito"),
            ft.dropdown.Option("paypal")
        ],
        value="contanti", width=300
    )
    data_inizio_field = ft.TextField(label="Data inizio (YYYY-MM-DD)", width=300, value=str(date.today()))
    data_fine_field = ft.TextField(label="Data fine (solo per noleggi)", width=300)
    message_text = ft.Text("", size=16, color="green")

    def handle_save(e):
        try:
            if not prodotto_dropdown.value:
                message_text.value = "⚠️ Seleziona un prodotto."
                message_text.color = "red"
                page.update()
                return

            if not quantita_field.value.isdigit() or int(quantita_field.value) <= 0:
                message_text.value = "⚠️ Inserisci una quantità valida."
                message_text.color = "red"
                page.update()
                return

            if tipo_operazione.value == "Noleggio" and not data_fine_field.value:
                message_text.value = "⚠️ Inserisci la data fine per il noleggio!"
                message_text.color = "red"
                page.update()
                return

            prodotto_id = int(prodotto_dropdown.value.split(" - ")[0])
            quantita = int(quantita_field.value)
            cliente = cliente_field.value.strip()

            db = SessionLocal()
            prodotto_corrente = [p for p in prodotti if p.id == prodotto_id][0]
            danneggiati = count_damages_for_product(db, prodotto_id)
            disponibili = max(0, prodotto_corrente.quantita - danneggiati)

            if quantita > disponibili:
                message_text.value = f"⚠️ Disponibili solo {disponibili} pezzi."
                message_text.color = "red"
                db.close()
                page.update()
                return

            if tipo_operazione.value == "Noleggio":
                noleggio = create_rental(db, RentalCreate(
                    prodotto_id=prodotto_id,
                    quantita=quantita,
                    cliente=cliente,
                    data_inizio=date.fromisoformat(data_inizio_field.value),
                    data_fine=date.fromisoformat(data_fine_field.value),
                    stato="in corso",
                    metodo_pagamento=metodo_pagamento.value
                ))
                create_notification(db, f"Noleggio per {cliente}", tipo="noleggio", operazione_id=noleggio.id)
            else:
                vendita = create_sale(db, SaleCreate(
                    prodotto_id=prodotto_id,
                    quantita=quantita,
                    cliente=cliente,
                    data_vendita=date.today(),
                    stato="confermato",
                    metodo_pagamento=metodo_pagamento.value
                ))
                create_notification(db, f"Vendita a {cliente}", tipo="vendita", operazione_id=vendita.id)

            update_quantity(db, prodotto_id, max(0, prodotto_corrente.quantita - quantita))
            db.close()
            message_text.value = f"✅ {tipo_operazione.value} registrato con successo!"
            message_text.color = "green"
        except Exception as ex:
            message_text.value = f"❌ Errore: {str(ex)}"
            message_text.color = "red"
        page.update()

    content = ft.Column([
        ft.Text("Registra Noleggio / Vendita", size=30, weight=ft.FontWeight.BOLD),
        ft.Row([tipo_operazione, prodotto_dropdown], spacing=10),
        ft.Row([quantita_field, cliente_field], spacing=10),
        metodo_pagamento, data_inizio_field, data_fine_field,
        ft.ElevatedButton("Registra", on_click=handle_save, width=250),
        message_text
    ], spacing=15, expand=True)

    return ft.View(
        route="/rental_sale",
        bgcolor="#1e90ff",
        controls=[
            ft.Row([
                build_menu(page),
                ft.Container(content=content, expand=True, bgcolor=ft.Colors.WHITE, padding=30, border_radius=15,
                             shadow=ft.BoxShadow(spread_radius=1, blur_radius=8,
                                                 color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK)))
            ], expand=True)
        ]
    )