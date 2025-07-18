import flet as ft
from app.models.database import SessionLocal
from app.services.rental_service import get_all_rentals
from app.services.sale_service import get_all_sales
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header

def history_page(page: ft.Page):
    # Controllo Autenticazione Utente
    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route="/history",
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

    # Connessione Al Database
    db = SessionLocal()
    rentals = get_all_rentals(db)
    sales = get_all_sales(db)
    db.close()

    # Dropdown Filtri
    filtro_tipo = ft.Dropdown(
        label="Visualizza",
        options=[
            ft.dropdown.Option("Noleggi"),
            ft.dropdown.Option("Vendite")
        ],
        value="Noleggi",
        width=200
    )
    filtro_ordinamento = ft.Dropdown(
        label="Ordina Per",
        options=[
            ft.dropdown.Option("Più Recenti"),
            ft.dropdown.Option("Meno Recenti")
        ],
        value="Più Recenti",
        width=200
    )
    ricerca_cliente = ft.TextField(label="Cerca Cliente", width=250)

    # Contenitore Principale Delle Card
    storico_column = ft.Column(
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH
    )

    # Funzione Per Creare Card
    def build_card(titolo: str, dettagli: list[str], colore: str):
        return ft.Container(
            content=ft.Column([
                ft.Text(titolo, size=16, weight=ft.FontWeight.BOLD, color=colore),
                *[ft.Text(d, size=14) for d in dettagli]
            ], spacing=5),
            bgcolor=ft.Colors.with_opacity(0.05, colore),
            padding=15,
            border_radius=10
        )

    # Refresh Lista
    def refresh_list(e=None):
        storico_column.controls.clear()

        tipo = filtro_tipo.value
        ordinamento = filtro_ordinamento.value
        ricerca = ricerca_cliente.value.lower() if ricerca_cliente.value else ""

        elementi = rentals if tipo == "Noleggi" else sales

        if tipo == "Noleggi":
            elementi = sorted(
                elementi,
                key=lambda x: x.data_inizio,
                reverse=(ordinamento == "Più Recenti")
            )
        else:
            elementi = sorted(
                elementi,
                key=lambda x: x.data_vendita,
                reverse=(ordinamento == "Più Recenti")
            )

        for elem in elementi:
            cliente = elem.cliente.lower()
            if ricerca and ricerca not in cliente:
                continue

            if tipo == "Noleggi":
                dettagli = [
                    f"Prodotto ID: {elem.prodotto_id}",
                    f"Quantità: {elem.quantita}",
                    f"Data Inizio: {elem.data_inizio.strftime('%Y-%m-%d')}",
                    f"Data Fine: {elem.data_fine.strftime('%Y-%m-%d')}",
                    f"Stato: {elem.stato}",
                    f"Metodo Pagamento: {elem.metodo_pagamento}"
                ]
                card = build_card(f"Noleggio di {elem.cliente}", dettagli, ft.Colors.BLUE)
            else:
                dettagli = [
                    f"Prodotto ID: {elem.prodotto_id}",
                    f"Quantità: {elem.quantita}",
                    f"Data Vendita: {elem.data_vendita.strftime('%Y-%m-%d')}",
                    f"Stato: {elem.stato}",
                    f"Metodo Pagamento: {elem.metodo_pagamento}"
                ]
                card = build_card(f"Vendita a {elem.cliente}", dettagli, ft.Colors.GREEN)

            storico_column.controls.append(card)

        page.update()

    filtro_tipo.on_change = refresh_list
    filtro_ordinamento.on_change = refresh_list
    ricerca_cliente.on_change = refresh_list
    refresh_list()

    # Contenuto Pagina
    content = ft.Column([
        build_header(page, "Storico Operazioni"),
        ft.Row([filtro_tipo, filtro_ordinamento, ricerca_cliente], spacing=10),
        storico_column
    ], spacing=20, expand=True)

    return ft.View(
        route="/history",
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