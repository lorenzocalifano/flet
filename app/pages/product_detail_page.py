import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import get_product_by_id
from app.services.damage_service import count_damages_for_product
from app.utils.menu_builder import build_menu

def product_detail_page(page: ft.Page):
    # Controllo Autenticazione Utente
    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route="/product_detail",
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
            route="/product_detail",
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
    danneggiati = count_damages_for_product(db, int(product_id))
    db.close()

    if not prodotto:
        return ft.View(
            route="/product_detail",
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

    disponibili = max(0, prodotto.quantita - danneggiati)
    stato = f"{disponibili}/{prodotto.quantita} disponibili (danneggiati: {danneggiati})"

    dettagli = ft.Column([
        ft.Text(f"Nome: {prodotto.nome}", size=18, weight=ft.FontWeight.BOLD),
        ft.Text(f"Categoria: {prodotto.categoria}", size=16),
        ft.Text(f"Modello: {prodotto.modello or 'N/A'}", size=16),
        ft.Text(f"Dimensione: {prodotto.dimensione or 'N/A'}", size=16),
        ft.Text(f"Brand: {prodotto.brand or 'N/A'}", size=16),
        ft.Text(f"Stato: {stato}", size=16)
    ], spacing=8)

    buttons = []
    if page.session.get("user_role") in ["RESPONSABILE", "MAGAZZINIERE"]:
        buttons.append(
            ft.ElevatedButton(
                "Modifica Prodotto",
                width=250,
                on_click=lambda e: page.go(f"/add_edit_product?product_id={prodotto.id}")
            )
        )

    content = ft.Column([
        ft.Text("Dettaglio Prodotto", size=30, weight=ft.FontWeight.BOLD),
        dettagli,
        *buttons,
        ft.ElevatedButton("Torna Al Catalogo", on_click=lambda e: page.go("/catalog"), width=250)
    ], spacing=15)

    return ft.View(
        route="/product_detail",
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