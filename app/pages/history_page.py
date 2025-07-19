import flet as ft
from datetime import datetime
from app.models.database import SessionLocal
from app.services.rental_service import get_all_rentals, conclude_rental, cancel_rental
from app.services.sale_service import get_all_sales
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header


def history_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    db = SessionLocal()
    rentals = get_all_rentals(db)
    sales = get_all_sales(db)
    db.close()

    history_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh_history():
        history_column.controls.clear()

        db = SessionLocal()
        rentals_ref = get_all_rentals(db)
        sales_ref = get_all_sales(db)
        db.close()

        for r in rentals_ref:
            stato_color = ft.Colors.GREEN if r.stato == "concluso" else (
                ft.Colors.RED if r.stato == "annullato" else ft.Colors.ORANGE
            )

            # Pulsanti visibili solo se "in corso"
            buttons = []
            if r.stato == "in corso":
                buttons = [
                    ft.ElevatedButton("Concludi", bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE,
                                      on_click=lambda e, rid=r.id: handle_conclude(rid)),
                    ft.ElevatedButton("Annulla", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE,
                                      on_click=lambda e, rid=r.id: handle_cancel(rid)),
                    ft.ElevatedButton("Modifica", bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE,
                                      on_click=lambda e, rid=r.id: page.go(f"/rental_edit?rental_id={rid}"))
                ]

            history_column.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Noleggio - {r.cliente}", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Prodotto ID: {r.prodotto_id} | Quantità: {r.quantita}", size=14),
                        ft.Text(f"Stato: {r.stato}", size=14, color=stato_color),
                        ft.Row(buttons, spacing=10)
                    ]),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY),
                    border_radius=8
                )
            )

        for s in sales_ref:
            stato_color = ft.Colors.GREEN if s.stato == "confermato" else ft.Colors.RED
            history_column.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Vendita - {s.cliente}", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Prodotto ID: {s.prodotto_id} | Quantità: {s.quantita}", size=14),
                        ft.Text(f"Stato: {s.stato}", size=14, color=stato_color)
                    ]),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY),
                    border_radius=8
                )
            )

        page.update()

    def handle_conclude(rental_id):
        db = SessionLocal()
        conclude_rental(db, rental_id)
        db.close()
        refresh_history()

    def handle_cancel(rental_id):
        db = SessionLocal()
        cancel_rental(db, rental_id)
        db.close()
        refresh_history()

    refresh_history()

    content = ft.Column([
        build_header(page, "Storico Operazioni"),
        history_column
    ], spacing=20, expand=True)

    return ft.View(
        route="/history",
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
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=8,
                                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK))
                )
            ], expand=True)
        ]
    )