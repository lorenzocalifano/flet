import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import create_product, get_product_by_id
from app.schemas.product_schema import ProductCreate
from app.utils.menu_builder import build_menu

def add_edit_product_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    if page.session.get("user_role") not in ["RESPONSABILE", "MAGAZZINIERE"]:
        page.go("/dashboard")
        return

    product_id = page.query.get("product_id")
    prodotto = None

    if product_id:
        db = SessionLocal()
        prodotto = get_product_by_id(db, int(product_id))
        db.close()

    nome_field = ft.TextField(label="Nome", value=prodotto.nome if prodotto else "", width=300)
    categoria_field = ft.TextField(label="Categoria", value=prodotto.categoria if prodotto else "", width=300)
    quantita_field = ft.TextField(label="Quantità", value=str(prodotto.quantita) if prodotto else "", width=300,
                                  keyboard_type=ft.KeyboardType.NUMBER)
    message_text = ft.Text("", size=16, color="green")

    def handle_save(e):
        if not nome_field.value or not categoria_field.value or not quantita_field.value:
            message_text.value = "Tutti i campi sono obbligatori!"
            message_text.color = "red"
            page.update()
            return

        db = SessionLocal()
        if prodotto:
            prodotto.nome = nome_field.value
            prodotto.categoria = categoria_field.value
            prodotto.quantita = int(quantita_field.value)
            db.commit()
            message_text.value = f"✅ Prodotto '{prodotto.nome}' aggiornato!"
        else:
            nuovo = create_product(db, ProductCreate(
                nome=nome_field.value,
                categoria=categoria_field.value,
                quantita=int(quantita_field.value)
            ))
            message_text.value = f"✅ Prodotto '{nuovo.nome}' aggiunto!"
        db.close()

        message_text.color = "green"
        page.update()

    content = ft.Column([
        ft.Text("Aggiungi / Modifica Prodotto", size=30, weight=ft.FontWeight.BOLD),
        nome_field, categoria_field, quantita_field,
        ft.ElevatedButton("Salva", on_click=handle_save, width=250),
        message_text
    ], spacing=15)

    return ft.View(
        route="/add_edit_product",
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