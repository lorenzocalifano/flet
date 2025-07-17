import flet as ft
from app.models.database import SessionLocal
from app.services.rental_service import get_all_rentals
from app.services.sale_service import get_all_sales
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header

def history_page(page: ft.Page):
    # imposto il tema unico, per ora lasciamo sempre Montserrat
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # prendo tutto subito
    db = SessionLocal()
    noleggi = get_all_rentals(db)
    vendite = get_all_sales(db)
    db.close()

    # === FILTRI IN ALTO ===
    # dropdown per scegliere tipo operazione, tanto mettiamo solo Noleggi e Vendite
    tipo_operazione = ft.Dropdown(
        label="Tipo Operazione",
        options=[
            ft.dropdown.Option("Noleggi"),
            ft.dropdown.Option("Vendite")
        ],
        value="Noleggi",  # di default mostriamo i noleggi
        width=200
    )

    # ordina per data, utile se ci sono tanti record
    ordine_data = ft.Dropdown(
        label="Ordina per data",
        options=[
            ft.dropdown.Option("Più recenti prima"),
            ft.dropdown.Option("Meno recenti prima")
        ],
        value="Più recenti prima",
        width=200
    )

    # ricerca per cliente, abbastanza basic ma fa il suo lavoro
    ricerca_cliente = ft.TextField(label="Cerca per cliente", width=250)

    # colonna con le operazioni (scrollabile perché se sono tante non vogliamo bloccarci)
    operazioni_column = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH  # full width, più bello
    )

    # helper per creare una "card" singola di storico
    def build_card(colore, dettagli):
        return ft.Container(
            content=ft.Column(dettagli, spacing=5),
            padding=15,
            bgcolor=ft.Colors.with_opacity(0.08, colore),
            border_radius=10,
        )

    # funzione che aggiorna dinamicamente la lista
    def refresh_list(e=None):
        operazioni_column.controls.clear()

        if tipo_operazione.value == "Noleggi":
            # ordino e filtro
            operazioni = sorted(
                noleggi,
                key=lambda n: n.data_inizio,
                reverse=True if ordine_data.value == "Più recenti prima" else False
            )
            for n in operazioni:
                if ricerca_cliente.value and ricerca_cliente.value.lower() not in n.cliente.lower():
                    continue  # skip se non matcha la ricerca
                operazioni_column.controls.append(
                    build_card(ft.Colors.BLUE, [
                        ft.Text("NOLEGGIO", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                        ft.Text(f"Cliente: {n.cliente}", size=14),
                        ft.Text(f"Prodotto ID: {n.prodotto_id}", size=14),
                        ft.Text(f"Quantità: {n.quantita}", size=14),
                        ft.Text(f"Metodo pagamento: {n.metodo_pagamento}", size=14),
                        ft.Text(f"Stato: {n.stato}", size=14),
                        ft.Text(f"Periodo: {n.data_inizio} → {n.data_fine}", size=14)
                    ])
                )
        else:
            operazioni = sorted(
                vendite,
                key=lambda v: v.data_vendita,
                reverse=True if ordine_data.value == "Più recenti prima" else False
            )
            for v in operazioni:
                if ricerca_cliente.value and ricerca_cliente.value.lower() not in v.cliente.lower():
                    continue
                operazioni_column.controls.append(
                    build_card(ft.Colors.GREEN, [
                        ft.Text("VENDITA", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                        ft.Text(f"Cliente: {v.cliente}", size=14),
                        ft.Text(f"Prodotto ID: {v.prodotto_id}", size=14),
                        ft.Text(f"Quantità: {v.quantita}", size=14),
                        ft.Text(f"Metodo pagamento: {v.metodo_pagamento}", size=14),
                        ft.Text(f"Stato: {v.stato}", size=14),
                        ft.Text(f"Data: {v.data_vendita}", size=14)
                    ])
                )
        page.update()

    # collego subito gli eventi per refresh dinamico (così filtra in tempo reale)
    tipo_operazione.on_change = refresh_list
    ordine_data.on_change = refresh_list
    ricerca_cliente.on_change = refresh_list

    refresh_list()  # inizializza subito la lista

    # === ASSEMBLA IL CONTENUTO ===
    content = ft.Column([
        build_header(page, "Storico Operazioni"),
        ft.Row([tipo_operazione, ordine_data, ricerca_cliente], spacing=15),
        operazioni_column
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