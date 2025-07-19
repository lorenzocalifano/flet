import flet as ft
from datetime import datetime, date
from app.models.database import SessionLocal
from app.services.rental_service import get_all_rentals, conclude_rental, cancel_rental
from app.services.sale_service import get_all_sales, cancel_sale
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header

def history_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    db = SessionLocal()
    try:
        noleggi = get_all_rentals(db)
        vendite = get_all_sales(db)
    finally:
        db.close()

    search_field = ft.TextField(label="Cerca cliente", width=300)
    filtro_tipo = ft.Dropdown(
        label="Tipo Operazione",
        options=[
            ft.dropdown.Option("Tutte"),
            ft.dropdown.Option("Noleggi"),
            ft.dropdown.Option("Vendite")
        ],
        value="Tutte",
        width=200
    )

    operazioni_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh_list(e=None):
        operazioni_column.controls.clear()

        db = SessionLocal()
        try:
            noleggi_correnti = get_all_rentals(db)
            vendite_correnti = get_all_sales(db)
        finally:
            db.close()

        query = search_field.value.lower() if search_field.value else ""
        tipo = filtro_tipo.value

        # Combino noleggi e vendite
        operazioni = []

        if tipo in ("Tutte", "Noleggi"):
            for n in noleggi_correnti:
                if query and query not in n.cliente.lower():
                    continue
                operazioni.append({
                    "tipo": "Noleggio",
                    "id": n.id,
                    "cliente": n.cliente,
                    "quantita": n.quantita,
                    "data": n.data_inizio.strftime("%Y-%m-%d"),
                    "stato": n.stato,
                    "metodo": n.metodo_pagamento
                })

        if tipo in ("Tutte", "Vendite"):
            for v in vendite_correnti:
                if query and query not in v.cliente.lower():
                    continue
                operazioni.append({
                    "tipo": "Vendita",
                    "id": v.id,
                    "cliente": v.cliente,
                    "quantita": v.quantita,
                    "data": v.data_vendita.strftime("%Y-%m-%d"),
                    "stato": v.stato,
                    "metodo": v.metodo_pagamento
                })

        # Ordino per data decrescente
        operazioni.sort(key=lambda x: x["data"], reverse=True)

        for op in operazioni:
            pulsanti = []

            if op["tipo"] == "Noleggio":
                # Concludi noleggio
                if op["stato"] == "in corso":
                    pulsanti.append(
                        ft.ElevatedButton(
                            "Concludi",
                            on_click=lambda e, oid=op["id"]: handle_conclude_rental(oid)
                        )
                    )
                # Annulla noleggio
                if op["stato"] == "in corso":
                    pulsanti.append(
                        ft.ElevatedButton(
                            "Annulla",
                            on_click=lambda e, oid=op["id"]: handle_cancel_rental(oid)
                        )
                    )
                # Modifica noleggio
                if op["stato"] == "in corso":
                    pulsanti.append(
                        ft.ElevatedButton(
                            "Modifica",
                            on_click=lambda e, oid=op["id"]: page.go(f"/rental_edit?rental_id={oid}")
                        )
                    )

            elif op["tipo"] == "Vendita":
                # Annulla vendita (solo se non già annullata)
                if op["stato"] == "confermato":
                    pulsanti.append(
                        ft.ElevatedButton(
                            "Annulla",
                            on_click=lambda e, oid=op["id"]: handle_cancel_sale(oid)
                        )
                    )

            operazioni_column.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(f"{op['tipo']} - {op['cliente']}", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                f"Quantità: {op['quantita']} | Data: {op['data']} | Stato: {op['stato']} | Metodo: {op['metodo']}",
                                size=12
                            )
                        ], expand=True),
                        ft.Row(pulsanti, spacing=5)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY),
                    border_radius=8
                )
            )
        page.update()

    def handle_conclude_rental(rental_id):
        db = SessionLocal()
        try:
            conclude_rental(db, rental_id)
        finally:
            db.close()
        refresh_list()

    def handle_cancel_rental(rental_id):
        db = SessionLocal()
        try:
            cancel_rental(db, rental_id)
        finally:
            db.close()
        refresh_list()

    def handle_cancel_sale(sale_id):
        db = SessionLocal()
        try:
            cancel_sale(db, sale_id)
        finally:
            db.close()
        refresh_list()

    # Collego i filtri
    search_field.on_change = refresh_list
    filtro_tipo.on_change = refresh_list

    refresh_list()

    content = ft.Column([
        build_header(page, "Storico Operazioni"),
        ft.Row([search_field, filtro_tipo], spacing=10),
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