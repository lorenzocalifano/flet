import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import get_all_products
from app.services.damage_service import count_damages_for_product
from app.utils.menu_builder import build_menu

def catalog_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    db = SessionLocal()
    prodotti = get_all_products(db)
    db.close()

    product_list_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh_list():
        db = SessionLocal()
        prodotti_refreshed = get_all_products(db)
        db.close()

        product_list_column.controls.clear()
        for p in prodotti_refreshed:
            db2 = SessionLocal()
            danneggiati = count_damages_for_product(db2, p.id)
            db2.close()

            disponibili = max(0, p.quantita - danneggiati)
            stato = f"{disponibili}/{p.quantita} disponibili (danneggiati: {danneggiati})"
            color = ft.Colors.WHITE if disponibili > 0 else ft.Colors.with_opacity(0.1, ft.Colors.RED)

            product_list_column.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(f"{p.nome} ({p.categoria})", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Modello: {p.modello or 'N/A'} | Dimensione: {p.dimensione or 'N/A'} | Brand: {p.brand or 'N/A'}", size=12, italic=True),
                            ft.Text(stato, size=14)
                        ], expand=True),
                        ft.ElevatedButton("Dettagli", on_click=lambda e, pid=p.id: page.go(f"/product_detail?product_id={pid}"))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=10,
                    bgcolor=color,
                    border_radius=10,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK))
                )
            )
        page.update()

    refresh_list()

    # ✅ Bottone flottante
    floating_button = None
    if page.session.get("user_role") in ["RESPONSABILE", "MAGAZZINIERE"]:
        floating_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.BLUE,
            on_click=lambda e: page.go("/add_edit_product")
        )

    content = ft.Stack([
        ft.Column([
            ft.Text("Catalogo Prodotti", size=30, weight=ft.FontWeight.BOLD),
            product_list_column
        ], spacing=20, expand=True),
        floating_button if floating_button else ft.Container()
    ])

    return ft.View(
        route="/catalog",
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