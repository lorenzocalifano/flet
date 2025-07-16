import flet as ft
from urllib.parse import parse_qs
from app.models.database import SessionLocal
from app.services.product_service import get_product_by_id, update_quantity

def quantity_update_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # Recupero l'ID del prodotto dall'URL
    query_params = parse_qs(page.route.split("?")[1]) if "?" in page.route else {}
    product_id = int(query_params.get("product_id", [0])[0])

    db = SessionLocal()
    prodotto = get_product_by_id(db, product_id)
    db.close()

    if not prodotto:
        return ft.View(
            route="/quantity_update",
            controls=[
                ft.Text("Prodotto non trovato", color="red", size=20),
                ft.ElevatedButton("Torna al Catalogo", on_click=lambda e: page.go("/catalog"))
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor="#1e90ff"
        )

    nuova_quantita_field = ft.TextField(
        label="Nuova Quantità",
        value=str(prodotto.quantita),
        width=200,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    message_text = ft.Text("", size=16, color="green")

    def handle_update(e):
        try:
            nuova_q = int(nuova_quantita_field.value)
            db = SessionLocal()
            update_quantity(db, prodotto.id, nuova_q)
            db.close()
            message_text.value = f"Quantità aggiornata con successo a {nuova_q}!"
        except ValueError:
            message_text.value = "Inserisci un numero valido."
        page.update()

    return ft.View(
        route="/quantity_update",
        controls=[
            ft.AppBar(title=ft.Text("Aggiorna Quantità"), center_title=True),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"{prodotto.nome}", size=25, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Quantità attuale: {prodotto.quantita}", size=18),
                        nuova_quantita_field,
                        ft.ElevatedButton("Aggiorna", on_click=handle_update, width=200),
                        message_text,
                        ft.ElevatedButton(
                            "Torna ai Dettagli",
                            on_click=lambda e: page.go(f"/product_detail?product_id={prodotto.id}"),
                            width=200
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