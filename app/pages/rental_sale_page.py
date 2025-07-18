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
    # imposto font unico
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route=page.route,
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text(
                            "⛔ Utente non autorizzato",
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

    # controllo i permessi, solo responsabile e segreteria possono usare questa pagina
    if page.session.get("user_role") not in ["RESPONSABILE", "SEGRETERIA"]:
        page.go("/dashboard")
        return

    # prendo tutti i prodotti
    db = SessionLocal()
    prodotti = get_all_products(db)
    db.close()

    # === CAMPI DEL FORM ===
    # dropdown con tutti i prodotti
    prodotto_dropdown = ft.Dropdown(
        label="Prodotto",
        options=[ft.dropdown.Option(str(p.id), f"{p.nome} ({p.categoria})") for p in prodotti],
        width=300
    )

    # scelta tra noleggio e vendita
    tipo_operazione = ft.Dropdown(
        label="Operazione",
        options=[ft.dropdown.Option("Noleggio"), ft.dropdown.Option("Vendita")],
        width=300
    )

    quantita_field = ft.TextField(label="Quantità", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    cliente_field = ft.TextField(label="Cliente", width=300)

    # metodo di pagamento, aggiungiamo i classici
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

    message_text = ft.Text("", size=16)  # messaggi di errore o successo

    # === FUNZIONE DI REGISTRAZIONE ===
    def handle_submit(e):
        # controlli base, un po' brutali ma per ora funzionano
        if not prodotto_dropdown.value or not tipo_operazione.value or not quantita_field.value \
                or not cliente_field.value or not metodo_pagamento.value:
            message_text.value = "⚠️ Tutti i campi sono obbligatori!"
            message_text.color = "red"
            page.update()
            return

        # controllo specifico per i noleggi (la data fine è fondamentale)
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
                # creo noleggio nel db
                create_rental(db, RentalCreate(
                    prodotto_id=prodotto_id,
                    quantita=quantita,
                    cliente=cliente_field.value,
                    data_inizio=date.fromisoformat(data_inizio.value),
                    data_fine=date.fromisoformat(data_fine.value),
                    stato="in corso",
                    metodo_pagamento=metodo_pagamento.value
                ))

                # creo notifica subito, così appare in lista
                create_notification(
                    db,
                    messaggio=f"Noleggio registrato: {cliente_field.value} ha noleggiato {quantita}x Prodotto ID {prodotto_id} "
                              f"({data_inizio.value} → {data_fine.value})",
                    tipo="noleggio",
                    operazione_id=prodotto_id
                )

            else:
                # creo vendita nel db
                create_sale(db, SaleCreate(
                    prodotto_id=prodotto_id,
                    quantita=quantita,
                    cliente=cliente_field.value,
                    data_vendita=date.fromisoformat(data_inizio.value),
                    stato="concluso",
                    metodo_pagamento=metodo_pagamento.value
                ))

                # e anche qui facciamo la notifica
                create_notification(
                    db,
                    messaggio=f"Vendita registrata: {cliente_field.value} ha acquistato {quantita}x Prodotto ID {prodotto_id} "
                              f"({metodo_pagamento.value})",
                    tipo="vendita",
                    operazione_id=prodotto_id
                )

            # aggiorniamo le quantità
            update_product_quantity(db, prodotto_id, -quantita)

            message_text.value = f"✅ {tipo_operazione.value} registrato con successo!"
            message_text.color = "green"

            # portiamo l'utente subito alle notifiche, così vede subito la nuova notifica
            page.go("/notifications")

        except Exception as ex:
            # gestiamo errori a caso
            message_text.value = f"❌ Errore: {str(ex)}"
            message_text.color = "red"
        finally:
            db.close()
        page.update()

    # === ASSEMBLA TUTTO ===
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