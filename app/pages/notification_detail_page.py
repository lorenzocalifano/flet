import flet as ft
from app.models.database import SessionLocal
from app.services.notification_service import get_notification_by_id, mark_notification_as_read
from app.services.rental_service import get_rental_by_id
from app.services.sale_service import get_sale_by_id
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header

def notification_detail_page(page: ft.Page):
    # Controllo Autenticazione Utente
    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route="/notification_detail",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text("Utente Non Autorizzato", size=22, color=ft.Colors.RED, weight=ft.FontWeight.BOLD),
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        alignment=ft.alignment.center
                    )
                ], expand=True)
            ]
        )

    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    try:
        notification_id = page.query.get("notification_id")
    except:
        notification_id = None

    if not notification_id:
        return ft.View(
            route="/notification_detail",
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text("Notifica Non Trovata", size=20, color="red"),
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        alignment=ft.alignment.center
                    )
                ], expand=True)
            ]
        )

    db = SessionLocal()
    notifica = get_notification_by_id(db, int(notification_id))
    operazione_dettagli = []

    if notifica:
        if notifica.tipo == "noleggio" and notifica.operazione_id:
            noleggio = get_rental_by_id(db, notifica.operazione_id)
            if noleggio:
                operazione_dettagli.extend([
                    ft.Text(f"Cliente: {noleggio.cliente}", size=16),
                    ft.Text(f"Quantità: {noleggio.quantita}", size=16),
                    ft.Text(f"Data Inizio: {noleggio.data_inizio}", size=16),
                    ft.Text(f"Data Fine: {noleggio.data_fine}", size=16),
                    ft.Text(f"Metodo Pagamento: {noleggio.metodo_pagamento}", size=16)
                ])
        elif notifica.tipo == "vendita" and notifica.operazione_id:
            vendita = get_sale_by_id(db, notifica.operazione_id)
            if vendita:
                operazione_dettagli.extend([
                    ft.Text(f"Cliente: {vendita.cliente}", size=16),
                    ft.Text(f"Quantità: {vendita.quantita}", size=16),
                    ft.Text(f"Data Vendita: {vendita.data_vendita}", size=16),
                    ft.Text(f"Metodo Pagamento: {vendita.metodo_pagamento}", size=16)
                ])
    db.close()

    content = ft.Column([
        build_header(page, "Dettaglio Notifica"),
        ft.Text(f"Messaggio: {notifica.messaggio}", size=18, weight=ft.FontWeight.BOLD),
        ft.Text(f"Data: {notifica.data_creazione.strftime('%Y-%m-%d %H:%M')}", size=16),
        ft.Text(f"Stato: {'Letta' if notifica.letto else 'Non Letta'}", size=16),
        ft.Column(operazione_dettagli if operazione_dettagli else [
            ft.Text("Nessun dettaglio aggiuntivo", size=16)
        ], spacing=5),
        ft.ElevatedButton("Segna Come Letta", on_click=lambda e: segna_letto(page, int(notification_id))),
        ft.ElevatedButton("Torna Alle Notifiche", on_click=lambda e: page.go("/notifications"))
    ], spacing=15)

    return ft.View(
        route="/notification_detail",
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

def segna_letto(page: ft.Page, notification_id: int):
    db = SessionLocal()
    try:
        mark_notification_as_read(db, notification_id)
    finally:
        db.close()
    page.go("/notifications")