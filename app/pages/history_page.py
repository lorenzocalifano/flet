import flet as ft
from app.models.database import SessionLocal
from app.services.rental_service import get_all_rentals
from app.services.sale_service import get_all_sales
from app.services.product_service import get_product_by_id

def history_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    if page.session.get("user_role") not in ["RESPONSABILE", "SEGRETERIA"]:
        page.go("/dashboard")
        return

    db = SessionLocal()
    noleggi = get_all_rentals(db)
    vendite = get_all_sales(db)
    db.close()

    menu_items = [
        ft.ElevatedButton("Dashboard", on_click=lambda e: page.go("/dashboard")),
        ft.ElevatedButton("Catalogo", on_click=lambda e: page.go("/catalog")),
        ft.ElevatedButton("Storico", on_click=lambda e: page.go("/history")),
        ft.ElevatedButton("Noleggi/Vendite", on_click=lambda e: page.go("/rental_sale")),
        ft.ElevatedButton("Notifiche", on_click=lambda e: page.go("/notifications"))
    ]
    if page.session.get("user_role") == "RESPONSABILE":
        menu_items.append(ft.ElevatedButton("Gestione Dipendenti", on_click=lambda e: page.go("/user_management")))

    operazioni_list = []
    db = SessionLocal()
    for n in noleggi:
        prodotto = get_product_by_id(db, n.prodotto_id)
        operazioni_list.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("NOLEGGIO", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.AMBER),
                    ft.Text(f"Cliente: {n.cliente}", size=14),
                    ft.Text(f"Prodotto: {prodotto.nome if prodotto else '-'}", size=14),
                    ft.Text(f"Quantità: {n.quantita}", size=14),
                    ft.Text(f"Metodo: {n.metodo_pagamento}", size=14),
                    ft.Text(f"Stato: {n.stato}", size=14)
                ]),
                padding=10, bgcolor=ft.colors.WHITE, border_radius=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.with_opacity(0.2, ft.colors.BLACK))
            )
        )
    for v in vendite:
        prodotto = get_product_by_id(db, v.prodotto_id)
        operazioni_list.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("VENDITA", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN),
                    ft.Text(f"Cliente: {v.cliente}", size=14),
                    ft.Text(f"Prodotto: {prodotto.nome if prodotto else '-'}", size=14),
                    ft.Text(f"Quantità: {v.quantita}", size=14),
                    ft.Text(f"Metodo: {v.metodo_pagamento}", size=14),
                    ft.Text(f"Stato: {v.stato}", size=14)
                ]),
                padding=10, bgcolor=ft.colors.WHITE, border_radius=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.with_opacity(0.2, ft.colors.BLACK))
            )
        )
    db.close()

    content = ft.Column([
        ft.Text("Storico Operazioni", size=30, weight=ft.FontWeight.BOLD),
        ft.Column(operazioni_list, spacing=10, scroll=ft.ScrollMode.AUTO)
    ], spacing=20)

    return ft.View(
        route="/history",
        bgcolor="#1e90ff",
        controls=[
            ft.Row([
                ft.Container(content=ft.Column(menu_items, spacing=10), width=220, bgcolor=ft.colors.BLUE_700, padding=15),
                ft.Container(content=content, expand=True, bgcolor=ft.colors.WHITE, padding=30, border_radius=15,
                             shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=ft.colors.with_opacity(0.25, ft.colors.BLACK)))
            ], expand=True)
        ]
    )