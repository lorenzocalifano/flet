import flet as ft
from datetime import date
from app.models.database import SessionLocal
from app.services.rental_service import get_rental_by_id, update_rental
from app.utils.menu_builder import build_menu


def rental_edit_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    rental_id = page.query.get("rental_id")
    if not rental_id:
        return ft.View(
            route="/rental_edit",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text("Noleggio non trovato", size=22, color="red", weight=ft.FontWeight.BOLD),
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        alignment=ft.alignment.center
                    )
                ], expand=True)
            ]
        )

    db = SessionLocal()
    noleggio = get_rental_by_id(db, int(rental_id))
    db.close()

    if not noleggio:
        return ft.View(
            route="/rental_edit",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text("Noleggio non trovato", size=22, color="red", weight=ft.FontWeight.BOLD),
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        alignment=ft.alignment.center
                    )
                ], expand=True)
            ]
        )

    # Campi modificabili
    quantita_field = ft.TextField(label="Quantità", value=str(noleggio.quantita), width=300)
    data_fine_field = ft.TextField(label="Data Fine (YYYY-MM-DD)", value=noleggio.data_fine.strftime("%Y-%m-%d"), width=300)
    metodo_field = ft.Dropdown(
        label="Metodo Pagamento",
        value=noleggio.metodo_pagamento,
        options=[
            ft.dropdown.Option("contanti"),
            ft.dropdown.Option("paypal"),
            ft.dropdown.Option("carta di credito")
        ],
        width=300
    )
    message_text = ft.Text("", size=16, color="green")

    def handle_update(e):
        try:
            nuova_data_fine = date.fromisoformat(data_fine_field.value)
            nuova_quantita = int(quantita_field.value)
            nuovo_metodo = metodo_field.value

            db = SessionLocal()
            try:
                # Controllo disponibilità direttamente dal service
                update_rental(
                    db,
                    noleggio.id,
                    quantita=nuova_quantita,
                    data_fine=nuova_data_fine,
                    metodo_pagamento=nuovo_metodo
                )
                message_text.value = "Noleggio aggiornato con successo"
                message_text.color = "green"
            except ValueError as ve:
                # Errore se supera i disponibili
                message_text.value = str(ve)
                message_text.color = "red"
            finally:
                db.close()
        except Exception as ex:
            message_text.value = f"Errore: {str(ex)}"
            message_text.color = "red"
        page.update()

    content = ft.Column([
        ft.Text("Modifica Noleggio", size=30, weight=ft.FontWeight.BOLD),
        quantita_field,
        data_fine_field,
        metodo_field,
        ft.ElevatedButton("Salva Modifiche", on_click=handle_update, width=250),
        message_text,
        ft.ElevatedButton("⬅ Torna allo Storico", on_click=lambda e: page.go("/history"), width=250)
    ], spacing=15)

    return ft.View(
        route="/rental_edit",
        bgcolor="#f0f8ff",
        controls=[
            ft.Row([
                build_menu(page),
                ft.Container(
                    content=content,
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    padding=30,
                    border_radius=15,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=8,
                                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK))
                )
            ], expand=True)
        ]
    )