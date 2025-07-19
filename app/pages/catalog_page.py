import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import get_all_products, delete_product
from app.services.damage_service import count_damages_for_product
from app.services.rental_service import get_all_rentals
from app.services.sale_service import get_all_sales
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header

def catalog_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # Recupera tutti i prodotti e operazioni
    db = SessionLocal()
    try:
        prodotti = get_all_products(db)
        noleggi = get_all_rentals(db)
        vendite = get_all_sales(db)
    finally:
        db.close()

    # Calcolo filtri unici
    categorie = sorted({p.categoria for p in prodotti if p.categoria})
    modelli = sorted({p.modello for p in prodotti if p.modello})
    dimensioni = sorted({p.dimensione for p in prodotti if p.dimensione})
    brands = sorted({p.brand for p in prodotti if p.brand})
    potenze = sorted({str(p.potenza) for p in prodotti if p.potenza})

    # Filtri
    categoria_filter = ft.Dropdown(label="Categoria", options=[ft.dropdown.Option(c) for c in categorie], width=200)
    modello_filter = ft.Dropdown(label="Modello", options=[ft.dropdown.Option(m) for m in modelli], width=200)
    dimensione_filter = ft.Dropdown(label="Dimensione", options=[ft.dropdown.Option(d) for d in dimensioni], width=200)
    brand_filter = ft.Dropdown(label="Brand", options=[ft.dropdown.Option(b) for b in brands], width=200)
    potenza_filter = ft.Dropdown(label="Potenza (W)", options=[ft.dropdown.Option(p) for p in potenze], width=200)
    search_field = ft.TextField(label="Cerca per nome", width=250)

    product_list_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh_list(e=None):
        product_list_column.controls.clear()

        db = SessionLocal()
        try:
            prodotti_refreshed = get_all_products(db)
            noleggi_refreshed = get_all_rentals(db)
            vendite_refreshed = get_all_sales(db)
        finally:
            db.close()

        for p in prodotti_refreshed:
            # Filtri
            if categoria_filter.value and p.categoria != categoria_filter.value:
                continue
            if modello_filter.value and p.modello != modello_filter.value:
                continue
            if dimensione_filter.value and p.dimensione != dimensione_filter.value:
                continue
            if brand_filter.value and p.brand != brand_filter.value:
                continue
            if potenza_filter.value and str(p.potenza) != potenza_filter.value:
                continue
            if search_field.value and search_field.value.lower() not in p.nome.lower():
                continue

            # Calcoli logici
            danneggiati = count_damages_for_product(SessionLocal(), p.id)
            venduti = sum(v.quantita for v in vendite_refreshed if v.prodotto_id == p.id)
            noleggiati = sum(n.quantita for n in noleggi_refreshed if n.prodotto_id == p.id and n.stato != "concluso")

            quantita_massima = max(0, p.quantita - venduti)
            disponibili = max(0, quantita_massima - danneggiati - noleggiati)

            stato = f"{disponibili}/{quantita_massima} disponibili (danneggiati: {danneggiati}, noleggiati: {noleggiati})"
            color = ft.Colors.WHITE if disponibili > 0 else ft.Colors.with_opacity(0.1, ft.Colors.RED)

            # Bottone elimina visibile solo per ruoli specifici
            elimina_btn = None
            if page.session.get("user_role") in ["RESPONSABILE", "MAGAZZINIERE"]:
                elimina_btn = ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color=ft.Colors.RED,
                    tooltip="Elimina Prodotto",
                    on_click=lambda e, pid=p.id: handle_delete(pid)
                )

            buttons_row = [
                ft.ElevatedButton("Dettagli", on_click=lambda e, pid=p.id: page.go(f"/product_detail?product_id={pid}"))
            ]
            if elimina_btn:
                buttons_row.append(elimina_btn)

            product_list_column.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(f"{p.nome} ({p.categoria})", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                f"Modello: {p.modello or 'N/A'} | Dimensione: {p.dimensione or 'N/A'} | "
                                f"Brand: {p.brand or 'N/A'} | Potenza: {p.potenza or 'N/A'} W",
                                size=12, italic=True
                            ),
                            ft.Text(stato, size=14)
                        ], expand=True),
                        ft.Row(buttons_row, spacing=10)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=10,
                    bgcolor=color,
                    border_radius=10,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5,
                                        color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK))
                )
            )
        page.update()

    def handle_delete(product_id):
        db = SessionLocal()
        try:
            delete_product(db, product_id)
        finally:
            db.close()
        refresh_list()

    for f in [categoria_filter, modello_filter, dimensione_filter, brand_filter, potenza_filter]:
        f.on_change = refresh_list
    search_field.on_change = refresh_list

    refresh_list()

    # Floating Button
    floating_button = None
    if page.session.get("user_role") in ["RESPONSABILE", "MAGAZZINIERE"]:
        floating_button = ft.Container(
            content=ft.FloatingActionButton(icon=ft.Icons.ADD, bgcolor=ft.Colors.BLUE,
                                            on_click=lambda e: page.go("/add_edit_product")),
            right=30, bottom=30
        )

    content = ft.Stack([
        ft.Column([
            build_header(page, "Catalogo Prodotti"),
            ft.Row([categoria_filter, modello_filter, dimensione_filter, brand_filter, search_field, potenza_filter], spacing=10),
            product_list_column
        ], spacing=20, expand=True),
        floating_button if floating_button else ft.Container()
    ], expand=True)

    return ft.View(
        route="/catalog",
        bgcolor="#f0f8ff",
        controls=[
            ft.Row([
                build_menu(page),
                ft.Container(
                    content=content,
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    padding=30,
                    border_radius=15,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=8,
                                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK))
                )
            ], expand=True)
        ]
    )