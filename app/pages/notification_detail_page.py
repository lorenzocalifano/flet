import flet as ft
from app.models.database import SessionLocal
from app.services.notification_service import get_notification_by_id, mark_notification_as_read
from app.services.rental_service import get_rental_by_id
from app.services.sale_service import get_sale_by_id
from app.utils.menu_builder import build_menu

def notification_detail_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    notification_id = int(page.query.get("notification_id"))
    db = SessionLocal()
    notifica = get_notification_by_id(db, notification_id)
    if notifica and not notifica.letto:
        mark_notification_as_read(db, notification_id)

    operazione_dettagli = []
    if notifica and notifica.tipo == "noleggio":
        n = get_rental_by_id(db, notifica.operazione_id)
        if n:
            operazione_dettagli.extend([
                ft.Text(f"Cliente: {n.cliente}", size=16),
                ft.Text(f"Quantità: {n.quantita}", size=16),
                ft.Text(f"Metodo pagamento: {n.metodo_pagamento}", size=16),
                ft.Text(f"Data inizio: {n.data_inizio}", size=16),
                ft.Text(f"Data fine: {n.data_fine}", size=16)
            ])
    elif notifica and notifica.tipo == "vendita":
        v = get_sale_by_id(db, notifica.operazione_id)
        if v:
            operazione_dettagli.extend([
                ft.Text(f"Cliente: {v.cliente}", size=16),
                ft.Text(f"Quantità: {v.quantita}", size=16),
                ft.Text(f"Metodo pagamento: {v.metodo_pagamento}", size=16),
                ft.Text(f"Data vendita: {v.data_vendita}", size=16)
            ])
    db.close()

    if not operazione_dettagli:
        operazione_dettagli.append(ft.Text("Nessun dettaglio aggiuntivo", size=16))

    content = ft.Column([
        ft.Text("Dettaglio Notifica", size=30, weight=ft.FontWeight.BOLD),
        ft.Text(f"Messaggio: {notifica.messaggio}", size=18),
        ft.Text(f"Data: {notifica.data_creazione}", size=16),
        *operazione_dettagli,
        ft.ElevatedButton("Torna alle Notifiche", on_click=lambda e: page.go("/notifications"), width=250)
    ], spacing=15)

    return ft.View(
        route="/notification_detail",
        bgcolor="#1e90ff",
        controls=[
            ft.Row([
                build_menu(page),
                ft.Container(content=content, expand=True, bgcolor=ft.colors.WHITE, padding=30, border_radius=15,
                             shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=ft.colors.with_opacity(0.25, ft.colors.BLACK)))
            ], expand=True)
        ]
    )