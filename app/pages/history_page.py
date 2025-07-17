import flet as ft
from app.models.database import SessionLocal
from app.services.rental_service import get_all_rentals
from app.services.sale_service import get_all_sales
from app.utils.menu_builder import build_menu

def history_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    db = SessionLocal()
    noleggi = get_all_rentals(db)
    vendite = get_all_sales(db)
    db.close()

    operazioni = []

    for n in noleggi:
        operazioni.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("NOLEGGIO", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                    ft.Text(f"Cliente: {n.cliente}", size=14),
                    ft.Text(f"Prodotto ID: {n.prodotto_id}", size=14),
                    ft.Text(f"Quantità: {n.quantita}", size=14),
                    ft.Text(f"Metodo pagamento: {n.metodo_pagamento}", size=14),
                    ft.Text(f"Stato: {n.stato}", size=14),
                    ft.Text(f"Periodo: {n.data_inizio} → {n.data_fine}", size=14)
                ], spacing=5),
                padding=15,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLUE),
                border_radius=10,
                expand=True
            )
        )

    for v in vendite:
        operazioni.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("VENDITA", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                    ft.Text(f"Cliente: {v.cliente}", size=14),
                    ft.Text(f"Prodotto ID: {v.prodotto_id}", size=14),
                    ft.Text(f"Quantità: {v.quantita}", size=14),
                    ft.Text(f"Metodo pagamento: {v.metodo_pagamento}", size=14),
                    ft.Text(f"Stato: {v.stato}", size=14),
                    ft.Text(f"Data: {v.data_vendita}", size=14)
                ], spacing=5),
                padding=15,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREEN),
                border_radius=10,
                expand=True
            )
        )

    content = ft.Column([
        ft.Text("Storico Operazioni", size=30, weight=ft.FontWeight.BOLD),
        ft.Column(operazioni, spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)
    ], spacing=20, expand=True)

    return ft.View(
        route="/history",
        bgcolor="#1e90ff",
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