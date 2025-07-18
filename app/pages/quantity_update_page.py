import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import get_product_by_id, update_product_quantity
from app.utils.menu_builder import build_menu

def quantity_update_page(page: ft.Page):
    # Controllo Autenticazione Utente
    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route="/quantity_update",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text(
                            "Utente Non Autorizzato",
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

    # Impostazione Tema
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # Recupero ID Prodotto
    try:
        product_id = page.query.get("product_id")
    except:
        product_id = None

    if not product_id:
        return ft.View(
            route="/quantity_update",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text("Prodotto Non Trovato", size=20, color="red"),
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        alignment=ft.alignment.center
                    )
                ], expand=True)
            ]
        )

    # Recupero Dati Prodotto
    db = SessionLocal()
    prodotto = get_product_by_id(db, int(product_id))
    db.close()

    if not prodotto:
        return ft.View(
            route="/quantity_update",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text("Prodotto Non Trovato", size=20, color="red"),
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        alignment=ft.alignment.center
                    )
                ], expand=True)
            ]
        )

    quantity_field = ft.TextField(label="Nuova Quantità", value=str(prodotto.quantita), width=200)
    message_text = ft.Text("", size=14)

    def handle_update(e):
        db = SessionLocal()
        try:
            update_product_quantity(db, prodotto.id, int(quantity_field.value))
            message_text.value = "Quantità Aggiornata Correttamente"
            message_text.color = "green"
        except Exception as ex:
            message_text.value = f"Errore: {str(ex)}"
            message_text.color = "red"
        finally:
            db.close()
        page.update()

    content = ft.Column([
        ft.Text("Aggiorna Quantità Prodotto", size=30, weight=ft.FontWeight.BOLD),
        ft.Text(f"Prodotto: {prodotto.nome}", size=18, weight=ft.FontWeight.BOLD),
        quantity_field,
        ft.ElevatedButton("Aggiorna Quantità", on_click=handle_update, width=250),
        message_text,
        ft.ElevatedButton("Torna Al Catalogo", on_click=lambda e: page.go("/catalog"), width=250)
    ], spacing=15)

    return ft.View(
        route="/quantity_update",
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
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK)
                    )
                )
            ], expand=True)
        ]
    )