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

    # ✅ Prepara opzioni uniche per i filtri
    categorie = sorted({p.categoria for p in prodotti if p.categoria})
    modelli = sorted({p.modello for p in prodotti if p.modello})
    dimensioni = sorted({p.dimensione for p in prodotti if p.dimensione})
    brands = sorted({p.brand for p in prodotti if p.brand})

    categoria_filter = ft.Dropdown(
        label="Categoria",
        options=[ft.dropdown.Option(c) for c in categorie],
        width=200
    )
    modello_filter = ft.Dropdown(
        label="Modello",
        options=[ft.dropdown.Option(m) for m in modelli],
        width=200
    )
    dimensione_filter = ft.Dropdown(
        label="Dimensione",
        options=[ft.dropdown.Option(d) for d in dimensioni],
        width=200
    )
    brand_filter = ft.Dropdown(
        label="Brand",
        options=[ft.dropdown.Option(b) for b in brands],
        width=200
    )

    product_list_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def update_list(e=None):
        db = SessionLocal()
        all_products = get_all_products(db)
        db.close()

        selected_categoria = categoria_filter.value
        selected_modello = modello_filter.value
        selected_dimensione = dimensione_filter.value
        selected_brand = brand_filter.value

        filtered = [
            p for p in all_products
            if (not selected_categoria or p.categoria == selected_categoria) and
               (not selected_modello or p.modello == selected_modello) and
               (not selected_dimensione or p.dimensione == selected_dimensione) and
               (not selected_brand or p.brand == selected_brand)
        ]

        product_list_column.controls.clear()

        db = SessionLocal()
        for p in filtered:
            danneggiati = count_damages_for_product(db, p.id)
            disponibili = max(0, p.quantita - danneggiati)
            stato = f"Disponibile ({disponibili}/{p.quantita})" if disponibili > 0 else f"NON disponibile ({danneggiati} danneggiati)"
            colore = ft.Colors.WHITE if disponibili > 0 else ft.Colors.with_opacity(0.2, ft.Colors.RED)
            product_list_column.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(f"{p.nome} ({p.categoria})", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Modello: {p.modello or 'N/A'} | Dimensione: {p.dimensione or 'N/A'} | Brand: {p.brand or 'N/A'}", size=12, italic=True),
                            ft.Text(stato, size=14)
                        ], expand=True),
                        ft.ElevatedButton("Dettagli",
                                          on_click=lambda e, pid=p.id: page.go(f"/product_detail?product_id={pid}"))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=10, bgcolor=colore, border_radius=10,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5,
                                        color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK))
                )
            )
        db.close()
        page.update()

    # ✅ Colleghiamo gli eventi di filtro
    categoria_filter.on_change = update_list
    modello_filter.on_change = update_list
    dimensione_filter.on_change = update_list
    brand_filter.on_change = update_list

    buttons = []
    if page.session.get("user_role") in ["RESPONSABILE", "MAGAZZINIERE"]:
        buttons.append(ft.ElevatedButton("➕ Aggiungi Prodotto",
                                         on_click=lambda e: page.go("/add_edit_product"),
                                         width=250))

    content = ft.Column([
        ft.Text("Catalogo Prodotti", size=30, weight=ft.FontWeight.BOLD),
        ft.Row([categoria_filter, modello_filter, dimensione_filter, brand_filter], spacing=10),
        *buttons,
        product_list_column
    ], spacing=20, expand=True)

    # ✅ Popola subito la lista
    update_list()

    return ft.View(
        route="/catalog",
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