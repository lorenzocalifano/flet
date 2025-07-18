import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import get_product_by_id
from app.services.damage_service import count_damages_for_product
from app.utils.menu_builder import build_menu

def product_detail_page(page: ft.Page):
    # solito tema, Montserrat ovunque per coerenza grafica
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

    # recupero product_id dalla querystring (TODO: forse va validato meglio)
    try:
        product_id = page.query.get("product_id")
    except:
        product_id = None

    # se non ho il product_id mostro un errore basic (potremmo farlo più carino)
    if not product_id:
        return ft.View(
            route="/product_detail",
            bgcolor="#1e90ff",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text("❌ Prodotto non trovato!", size=20, color="red"),
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        padding=30,
                        border_radius=15
                    )
                ], expand=True)
            ]
        )

    # prendo il prodotto dal db
    db = SessionLocal()
    prodotto = get_product_by_id(db, int(product_id))
    danneggiati = count_damages_for_product(db, int(product_id))
    db.close()

    if not prodotto:
        # stessa schermata d'errore se il prodotto non esiste
        return ft.View(
            route="/product_detail",
            bgcolor="#1e90ff",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text("❌ Prodotto non trovato!", size=20, color="red"),
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        padding=30,
                        border_radius=15
                    )
                ], expand=True)
            ]
        )

    # calcolo disponibili e preparo lo stato
    disponibili = max(0, prodotto.quantita - danneggiati)
    stato = f"{disponibili}/{prodotto.quantita} disponibili (danneggiati: {danneggiati})"

    # dettagli del prodotto in colonna
    dettagli = ft.Column([
        ft.Text(f"Nome: {prodotto.nome}", size=18, weight=ft.FontWeight.BOLD),
        ft.Text(f"Categoria: {prodotto.categoria}", size=16),
        ft.Text(f"Modello: {prodotto.modello or 'N/A'}", size=16),
        ft.Text(f"Dimensione: {prodotto.dimensione or 'N/A'}", size=16),
        ft.Text(f"Brand: {prodotto.brand or 'N/A'}", size=16),
        ft.Text(f"Stato: {stato}", size=16)
    ], spacing=8)

    # bottone per modificare il prodotto (solo per ruoli con permessi)
    buttons = []
    if page.session.get("user_role") in ["RESPONSABILE", "MAGAZZINIERE"]:
        buttons.append(
            ft.ElevatedButton(
                "Modifica Prodotto",
                width=250,
                on_click=lambda e: page.go(f"/add_edit_product?product_id={prodotto.id}")
            )
        )

    # assemblo il contenuto principale
    content = ft.Column([
        ft.Text("Dettaglio Prodotto", size=30, weight=ft.FontWeight.BOLD),
        dettagli,
        *buttons,
        ft.ElevatedButton("⬅ Torna al Catalogo", on_click=lambda e: page.go("/catalog"), width=250)
    ], spacing=15)

    return ft.View(
        route="/product_detail",
        bgcolor="#1e90ff",  # sfondo blu tenue per coerenza con il resto
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