import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import create_product, get_product_by_id
from app.schemas.product_schema import ProductCreate
from app.utils.menu_builder import build_menu

def add_edit_product_page(page: ft.Page):
    # solito font, manteniamo coerenza ovunque
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # solo responsabile e magazziniere possono aggiungere/modificare prodotti
    if page.session.get("user_role") not in ["RESPONSABILE", "MAGAZZINIERE"]:
        page.go("/dashboard")
        return

    # recupero product_id se passato, serve per capire se stiamo modificando o aggiungendo
    try:
        product_id = page.query.get("product_id")
    except:
        product_id = None

    # se stiamo modificando, recuperiamo il prodotto dal db
    prodotto = None
    if product_id:
        db = SessionLocal()
        prodotto = get_product_by_id(db, int(product_id))
        db.close()

    # === CAMPI FORM ===
    # se esiste un prodotto, precompiliamo i campi con i suoi valori
    nome_field = ft.TextField(label="Nome", value=prodotto.nome if prodotto else "", width=300)
    categoria_field = ft.TextField(label="Categoria", value=prodotto.categoria if prodotto else "", width=300)
    quantita_field = ft.TextField(
        label="Quantità",
        value=str(prodotto.quantita) if prodotto else "",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    modello_field = ft.TextField(
        label="Modello",
        value=prodotto.modello if prodotto and prodotto.modello else "",
        width=300
    )
    dimensione_field = ft.TextField(
        label="Dimensione",
        value=prodotto.dimensione if prodotto and prodotto.dimensione else "",
        width=300
    )
    brand_field = ft.TextField(
        label="Brand",
        value=prodotto.brand if prodotto and prodotto.brand else "",
        width=300
    )

    message_text = ft.Text("", size=16, color="green")

    # === FUNZIONE DI SALVATAGGIO ===
    def handle_save(e):
        # controlli
        if not nome_field.value or not categoria_field.value or not quantita_field.value:
            message_text.value = "⚠️ Nome, Categoria e Quantità sono obbligatori!"
            message_text.color = "red"
            page.update()
            return

        db = SessionLocal()
        try:
            if prodotto:
                # siamo in modalità modifica: aggiorniamo il prodotto
                prodotto_db = get_product_by_id(db, prodotto.id)  # TODO: forse inutile, ma meglio ricaricare da db
                if prodotto_db:
                    prodotto_db.nome = nome_field.value
                    prodotto_db.categoria = categoria_field.value
                    prodotto_db.quantita = int(quantita_field.value)
                    prodotto_db.modello = modello_field.value or None
                    prodotto_db.dimensione = dimensione_field.value or None
                    prodotto_db.brand = brand_field.value or None

                    db.commit()
                    db.refresh(prodotto_db)
                    message_text.value = f"✅ Prodotto '{prodotto_db.nome}' aggiornato!"
            else:
                # modalità aggiunta: creiamo nuovo prodotto
                nuovo = create_product(db, ProductCreate(
                    nome=nome_field.value,
                    categoria=categoria_field.value,
                    quantita=int(quantita_field.value),
                    modello=modello_field.value or None,
                    dimensione=dimensione_field.value or None,
                    brand=brand_field.value or None
                ))
                message_text.value = f"✅ Prodotto '{nuovo.nome}' aggiunto!"

            message_text.color = "green"
        except Exception as ex:
            # TODO: gestire meglio errori (es. nome duplicato? categoria inesistente?)
            message_text.value = f"❌ Errore: {str(ex)}"
            message_text.color = "red"
        finally:
            db.close()

        page.update()

    # === ASSEMBLA IL CONTENUTO ===
    content = ft.Column([
        ft.Text("Aggiungi / Modifica Prodotto", size=30, weight=ft.FontWeight.BOLD),
        nome_field,
        categoria_field,
        quantita_field,
        modello_field,
        dimensione_field,
        brand_field,
        ft.ElevatedButton("Salva", on_click=handle_save, width=250),
        message_text,
        ft.ElevatedButton("⬅ Torna al Catalogo", on_click=lambda e: page.go("/catalog"), width=250)
    ], spacing=15)

    return ft.View(
        route="/add_edit_product",
        bgcolor="#1e90ff",  # sfondo coerente con le altre pagine gestionali
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