import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import create_product, get_product_by_id
from app.schemas.product_schema import ProductCreate
from app.utils.menu_builder import build_menu

def add_edit_product_page(page: ft.Page):
    # Controllo Autenticazione Utente
    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route="/add_edit_product",
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

    # Impostazione Tema Grafico
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # Recupero Sicuro Product Id Dalla Route
    product_id = None
    if "product_id=" in page.route:
        try:
            product_id = int(page.route.split("product_id=")[1])
        except:
            product_id = None

    # Caricamento Prodotto Se In Modalità Modifica
    prodotto = None
    if product_id:
        db = SessionLocal()
        prodotto = get_product_by_id(db, product_id)
        db.close()

    # Campi Del Form
    nome_field = ft.TextField(label="Nome", value=prodotto.nome if prodotto else "", width=300)
    categoria_field = ft.TextField(label="Categoria", value=prodotto.categoria if prodotto else "", width=300)
    quantita_field = ft.TextField(
        label="Quantità",
        value=str(prodotto.quantita) if prodotto else "",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    modello_field = ft.TextField(label="Modello", value=prodotto.modello or "" if prodotto else "", width=300)
    dimensione_field = ft.TextField(label="Dimensione", value=prodotto.dimensione or "" if prodotto else "", width=300)
    brand_field = ft.TextField(label="Brand", value=prodotto.brand or "" if prodotto else "", width=300)
    message_text = ft.Text("", size=16, color="green")

    # Funzione Per Salvataggio
    def handle_save(e):
        if not nome_field.value or not categoria_field.value or not quantita_field.value:
            message_text.value = "Nome, Categoria e Quantità Sono Obbligatori"
            message_text.color = "red"
            page.update()
            return

        db = SessionLocal()
        try:
            if prodotto:
                # Modalità Aggiornamento Prodotto
                prodotto_db = get_product_by_id(db, prodotto.id)
                if prodotto_db:
                    prodotto_db.nome = nome_field.value
                    prodotto_db.categoria = categoria_field.value
                    prodotto_db.quantita = int(quantita_field.value)
                    prodotto_db.modello = modello_field.value or None
                    prodotto_db.dimensione = dimensione_field.value or None
                    prodotto_db.brand = brand_field.value or None
                    db.commit()
                    db.refresh(prodotto_db)
                    message_text.value = f"Prodotto '{prodotto_db.nome}' Aggiornato Correttamente"
            else:
                # Modalità Aggiunta Nuovo Prodotto
                nuovo = create_product(db, ProductCreate(
                    nome=nome_field.value,
                    categoria=categoria_field.value,
                    quantita=int(quantita_field.value),
                    modello=modello_field.value or None,
                    dimensione=dimensione_field.value or None,
                    brand=brand_field.value or None
                ))
                message_text.value = f"Prodotto '{nuovo.nome}' Aggiunto Correttamente"

            message_text.color = "green"
        except Exception as ex:
            message_text.value = f"Errore: {str(ex)}"
            message_text.color = "red"
        finally:
            db.close()

        page.update()

    # Contenuto Pagina
    content = ft.Column([
        ft.Text("Aggiungi O Modifica Prodotto", size=30, weight=ft.FontWeight.BOLD),
        nome_field, categoria_field, quantita_field,
        modello_field, dimensione_field, brand_field,
        ft.ElevatedButton("Salva", on_click=handle_save, width=250),
        message_text,
        ft.ElevatedButton("Torna Al Catalogo", on_click=lambda e: page.go("/catalog"), width=250)
    ], spacing=15)

    return ft.View(
        route="/add_edit_product",
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