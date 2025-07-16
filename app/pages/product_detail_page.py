import flet as ft
from urllib.parse import parse_qs
from app.models.database import SessionLocal
from app.services.product_service import get_product_by_id
from app.services.damage_service import count_damages_for_product

def product_detail_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # ✅ Recupero l'ID del prodotto dall'URL
    query_params = parse_qs(page.route.split("?")[1]) if "?" in page.route else {}
    product_id = int(query_params.get("product_id", [0])[0])

    db = SessionLocal()
    prodotto = get_product_by_id(db, product_id)
    danneggiati = count_damages_for_product(db, product_id)
    db.close()

    if not prodotto:
        return ft.View(
            route="/product_detail",
            controls=[
                ft.Text("Prodotto non trovato", color="red", size=20),
                ft.ElevatedButton("Torna al Catalogo", on_click=lambda e: page.go("/catalog"))
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor="#1e90ff"
        )

    disponibili_effettivi = max(0, prodotto.quantita - danneggiati)
    stato = (
        f"Disponibile ({disponibili_effettivi}/{prodotto.quantita})"
        if disponibili_effettivi > 0 else
        f"NON disponibile ({danneggiati} danneggiati)"
    )

    return ft.View(
        route="/product_detail",
        controls=[
            ft.AppBar(title=ft.Text("Dettagli Prodotto"), center_title=True),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"{prodotto.nome}", size=25, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Categoria: {prodotto.categoria}", size=18),
                        ft.Text(f"Brand: {prodotto.brand or '-'}", size=18),
                        ft.Text(f"Modello: {prodotto.modello or '-'}", size=18),
                        ft.Text(f"Potenza: {prodotto.potenza or '-'}", size=18),
                        ft.Text(f"Dimensione: {prodotto.dimensione or '-'}", size=18),
                        ft.Text(f"Quantità Totale: {prodotto.quantita}", size=18),
                        ft.Text(f"Danneggiati: {danneggiati}", size=18, color="red" if danneggiati > 0 else "black"),
                        ft.Text(f"Stato: {stato}", size=18),
                        ft.Divider(),
                        ft.ElevatedButton(
                            "Aggiorna Quantità",
                            on_click=lambda e: page.go(f"/quantity_update?product_id={prodotto.id}"),
                            width=250,
                            disabled=disponibili_effettivi == 0  # ✅ disabilitato se tutti rotti
                        ),
                        ft.ElevatedButton(
                            "Torna al Catalogo",
                            on_click=lambda e: page.go("/catalog"),
                            width=250
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                alignment=ft.alignment.center,
                padding=30,
                width=400,
                bgcolor=ft.colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=8,
                    color=ft.colors.with_opacity(0.25, ft.colors.BLACK),
                    offset=ft.Offset(0, 4)
                )
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor="#1e90ff"
    )