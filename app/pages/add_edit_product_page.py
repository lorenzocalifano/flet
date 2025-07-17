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

    try:
        product_id = page.query.get("product_id")
    except:
        product_id = None

    prodotto = None
    error_message = None

    if product_id:
        try:
            db = SessionLocal()
            prodotto = get_product_by_id(db, int(product_id))
            db.close()
            if not prodotto:
                error_message = f"❌ Prodotto con ID {product_id} non trovato!"
        except Exception as e:
            error_message = f"❌ Errore nel recupero del prodotto: {str(e)}"

    # ✅ Campi
    nome_field = ft.TextField(label="Nome", value=prodotto.nome if prodotto else "", width=300)
    categoria_field = ft.TextField(label="Categoria", value=prodotto.categoria if prodotto else "", width=300)
    quantita_field = ft.TextField(label="Quantità", value=str(prodotto.quantita) if prodotto else "", width=300,
                                  keyboard_type=ft.KeyboardType.NUMBER)
    modello_field = ft.TextField(label="Modello", value=prodotto.modello if prodotto and prodotto.modello else "", width=300)
    dimensione_field = ft.TextField(label="Dimensione", value=prodotto.dimensione if prodotto and prodotto.dimensione else "", width=300)
    brand_field = ft.TextField(label="Brand", value=prodotto.brand if prodotto and prodotto.brand else "", width=300)
    message_text = ft.Text("", size=16, color="green")

    def handle_save(e):
        if not nome_field.value or not categoria_field.value or not quantita_field.value:
            message_text.value = "⚠️ Tutti i campi obbligatori (Nome, Categoria e Quantità) devono essere compilati!"
            message_text.color = "red"
            page.update()
            return

        db = SessionLocal()
        try:
            if prodotto:
                prodotto.nome = nome_field.value
                prodotto.categoria = categoria_field.value
                prodotto.quantita = int(quantita_field.value)
                prodotto.modello = modello_field.value if modello_field.value else None
                prodotto.dimensione = dimensione_field.value if dimensione_field.value else None
                prodotto.brand = brand_field.value if brand_field.value else None
                db.commit()
                message_text.value = f"✅ Prodotto '{prodotto.nome}' aggiornato!"
            else:
                nuovo = create_product(db, ProductCreate(
                    nome=nome_field.value,
                    categoria=categoria_field.value,
                    quantita=int(quantita_field.value),
                    modello=modello_field.value if modello_field.value else None,
                    dimensione=dimensione_field.value if dimensione_field.value else None,
                    brand=brand_field.value if brand_field.value else None
                ))
                message_text.value = f"✅ Prodotto '{nuovo.nome}' aggiunto!"
            message_text.color = "green"
        except Exception as ex:
            message_text.value = f"❌ Errore: {str(ex)}"
            message_text.color = "red"
        finally:
            db.close()
        page.update()

    content_controls = [
        ft.Text("Aggiungi / Modifica Prodotto", size=30, weight=ft.FontWeight.BOLD),
    ]

    if error_message:
        content_controls.append(ft.Text(error_message, size=16, color="red"))
    else:
        content_controls.extend([
            nome_field, categoria_field, quantita_field,
            modello_field, dimensione_field, brand_field,
            ft.ElevatedButton("Salva", on_click=handle_save, width=250),
            message_text
        ])

    content_controls.append(
        ft.ElevatedButton("⬅ Torna al Catalogo", on_click=lambda e: page.go("/catalog"), width=250)
    )

    content = ft.Column(content_controls, spacing=15)

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