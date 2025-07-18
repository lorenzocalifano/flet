import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import get_product_by_id, update_product_quantity
from app.utils.menu_builder import build_menu

def quantity_update_page(page: ft.Page):
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

    if page.session.get("user_role") not in ["RESPONSABILE", "MAGAZZINIERE"]:
        page.go("/dashboard")
        return

    product_id = int(page.query.get("product_id"))
    db = SessionLocal()
    prodotto = get_product_by_id(db, product_id)
    db.close()

    quantita_field = ft.TextField(label="Nuova Quantità", value=str(prodotto.quantita), width=300, keyboard_type=ft.KeyboardType.NUMBER)
    message_text = ft.Text("", size=16, color="green")

    def handle_update(e):
        db = SessionLocal()
        update_quantity(db, product_id, int(quantita_field.value))
        db.close()
        message_text.value = "✅ Quantità aggiornata!"
        message_text.color = "green"
        page.update()

    content = ft.Column([
        ft.Text("Aggiorna Quantità Prodotto", size=30, weight=ft.FontWeight.BOLD),
        ft.Text(f"Prodotto: {prodotto.nome}", size=18),
        quantita_field,
        ft.ElevatedButton("Aggiorna", on_click=handle_update, width=250),
        message_text
    ], spacing=15)

    return ft.View(
        route="/quantity_update",
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