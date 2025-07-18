import flet as ft
from app.models.database import SessionLocal
from app.services.notification_service import get_notification_by_id, mark_notification_as_read
from app.services.rental_service import get_rental_by_id
from app.services.sale_service import get_sale_by_id
from app.utils.menu_builder import build_menu

def notification_detail_page(page: ft.Page):
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

    notification_id = int(page.query.get("notification_id"))
    db = SessionLocal()
    notifica = get_notification_by_id(db, notification_id)

    operazione_dettagli = []
    if notifica.tipo == "noleggio":
        n = get_rental_by_id(db, notifica.operazione_id)
        if n:
            operazione_dettagli.extend([
                ft.Text(f"Cliente: {n.cliente}", size=16),
                ft.Text(f"Prodotto ID: {n.prodotto_id}", size=16),
                ft.Text(f"Quantità: {n.quantita}", size=16),
                ft.Text(f"Metodo pagamento: {n.metodo_pagamento}", size=16),
                ft.Text(f"Periodo: {n.data_inizio} → {n.data_fine}", size=16),
                ft.Text(f"Stato: {n.stato}", size=16)
            ])
    elif notifica.tipo == "vendita":
        v = get_sale_by_id(db, notifica.operazione_id)
        if v:
            operazione_dettagli.extend([
                ft.Text(f"Cliente: {v.cliente}", size=16),
                ft.Text(f"Prodotto ID: {v.prodotto_id}", size=16),
                ft.Text(f"Quantità: {v.quantita}", size=16),
                ft.Text(f"Metodo pagamento: {v.metodo_pagamento}", size=16),
                ft.Text(f"Data vendita: {v.data_vendita}", size=16),
                ft.Text(f"Stato: {v.stato}", size=16)
            ])
    db.close()

    # Se non ci sono dettagli, aggiungiamo un messaggio generico
    if not operazione_dettagli:
        operazione_dettagli.append(ft.Text("Nessun dettaglio aggiuntivo", size=16))

    def handle_mark_read(e):
        db = SessionLocal()
        mark_notification_as_read(db, notification_id)
        db.close()
        page.go("/notifications")

    content = ft.Column([
        ft.Text("Dettaglio Notifica", size=30, weight=ft.FontWeight.BOLD),
        ft.Text(f"Messaggio: {notifica.messaggio}", size=18),
        ft.Text(f"Data: {notifica.data_creazione}", size=16),
        *operazione_dettagli,
        ft.Row([
            ft.ElevatedButton("Segna come letta", on_click=handle_mark_read, width=200),
            ft.ElevatedButton("Torna alle Notifiche", on_click=lambda e: page.go("/notifications"), width=200)
        ], spacing=10)
    ], spacing=15)

    return ft.View(
        route="/notification_detail",
        bgcolor="#1e90ff",
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