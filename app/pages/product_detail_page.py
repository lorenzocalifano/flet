import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import get_product_by_id
from app.services.damage_service import count_damages_for_product
from app.utils.menu_builder import build_menu

def product_detail_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    product_id = int(page.query.get("product_id"))
    db = SessionLocal()
    prodotto = get_product_by_id(db, product_id)
    danneggiati = count_damages_for_product(db, product_id)
    db.close()

    disponibili = max(0, prodotto.quantita - danneggiati)

    content = ft.Column([
        ft.Text("Dettaglio Prodotto", size=30, weight=ft.FontWeight.BOLD),
        ft.Text(f"Nome: {prodotto.nome}", size=18),
        ft.Text(f"Categoria: {prodotto.categoria}", size=16),
        ft.Text(f"Quantità totale: {prodotto.quantita}", size=16),
        ft.Text(f"Disponibili: {disponibili} / {prodotto.quantita}",
                size=16, color=ft.Colors.GREEN if disponibili > 0 else ft.Colors.RED),
        ft.ElevatedButton("Torna al Catalogo", on_click=lambda e: page.go("/catalog"), width=250)
    ], spacing=10)

    # ✅ Pulsante Modifica solo per Responsabile/Magazziniere
    if page.session.get("user_role") in ["RESPONSABILE", "MAGAZZINIERE"]:
        content.controls.append(
            ft.ElevatedButton(
                "✏️ Modifica Prodotto",
                on_click=lambda e: page.go(f"/add_edit_product?product_id={product_id}"),
                width=250
            )
        )

    return ft.View(
        route="/product_detail",
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