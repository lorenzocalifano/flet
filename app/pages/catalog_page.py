import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import get_all_products
from app.services.damage_service import count_damages_for_product

def catalog_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    db = SessionLocal()
    prodotti = get_all_products(db)
    db.close()

    user_role = page.session.get("user_role") or "MAGAZZINIERE"

    menu_items = [
        ft.ElevatedButton("Dashboard", on_click=lambda e: page.go("/dashboard")),
        ft.ElevatedButton("Catalogo", on_click=lambda e: page.go("/catalog")),
        ft.ElevatedButton("Notifiche", on_click=lambda e: page.go("/notifications"))
    ]
    if user_role in ["RESPONSABILE", "SEGRETERIA"]:
        menu_items.append(ft.ElevatedButton("Storico", on_click=lambda e: page.go("/history")))
        menu_items.append(ft.ElevatedButton("Noleggi/Vendite", on_click=lambda e: page.go("/rental_sale")))
    if user_role == "RESPONSABILE":
        menu_items.append(ft.ElevatedButton("Gestione Dipendenti", on_click=lambda e: page.go("/user_management")))
    if user_role in ["RESPONSABILE", "MAGAZZINIERE"]:
        menu_items.append(ft.ElevatedButton("Danni", on_click=lambda e: page.go("/damage_report")))

    product_list = []
    db = SessionLocal()
    for p in prodotti:
        danneggiati = count_damages_for_product(db, p.id)
        disponibili = max(0, p.quantita - danneggiati)
        stato = f"Disponibile ({disponibili}/{p.quantita})" if disponibili > 0 else f"NON disponibile ({danneggiati} danneggiati)"
        colore = ft.colors.WHITE if disponibili > 0 else ft.colors.with_opacity(0.2, ft.colors.RED)
        product_list.append(
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(f"{p.nome} ({p.categoria})", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(stato, size=14)
                    ]),
                    ft.ElevatedButton("Dettagli", on_click=lambda e, pid=p.id: page.go(f"/product_detail?product_id={pid}"),
                                      disabled=disponibili == 0)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=10, bgcolor=colore, border_radius=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.with_opacity(0.2, ft.colors.BLACK))
            )
        )
    db.close()

    content = ft.Column([ft.Text("Catalogo Prodotti", size=30, weight=ft.FontWeight.BOLD),
                         ft.Column(product_list, spacing=10, scroll=ft.ScrollMode.AUTO)], spacing=20)

    return ft.View(
        route="/catalog",
        bgcolor="#1e90ff",
        controls=[
            ft.Row([
                ft.Container(content=ft.Column(menu_items, spacing=10), width=220, bgcolor=ft.colors.BLUE_700, padding=15),
                ft.Container(content=content, expand=True, bgcolor=ft.colors.WHITE, padding=30, border_radius=15,
                             shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=ft.colors.with_opacity(0.25, ft.colors.BLACK)))
            ], expand=True)
        ]
    )