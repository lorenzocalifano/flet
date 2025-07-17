import flet as ft
from app.models.database import SessionLocal
from app.services.notification_service import get_all_notifications
from app.services.rental_service import get_rental_by_id
from app.services.sale_service import get_sale_by_id
from app.utils.menu_builder import build_menu

def notifications_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    db = SessionLocal()
    notifiche = get_all_notifications(db)

    notifiche_list = []
    for n in notifiche:
        dettagli = []
        if n.tipo == "noleggio":
            r = get_rental_by_id(db, n.operazione_id)
            if r:
                dettagli = [
                    ft.Text(f"Cliente: {r.cliente}", size=12),
                    ft.Text(f"Quantità: {r.quantita}", size=12),
                    ft.Text(f"Metodo pagamento: {r.metodo_pagamento}", size=12),
                    ft.Text(f"Periodo: {r.data_inizio} → {r.data_fine}", size=12)
                ]
        elif n.tipo == "vendita":
            v = get_sale_by_id(db, n.operazione_id)
            if v:
                dettagli = [
                    ft.Text(f"Cliente: {v.cliente}", size=12),
                    ft.Text(f"Quantità: {v.quantita}", size=12),
                    ft.Text(f"Metodo pagamento: {v.metodo_pagamento}", size=12),
                    ft.Text(f"Data vendita: {v.data_vendita}", size=12)
                ]

        stato = "Letta ✅" if n.letto else "Non letta 🔔"
        notifiche_list.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(n.messaggio, size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Stato: {stato}", size=12),
                    ft.Text(f"Data: {n.data_creazione.strftime('%Y-%m-%d %H:%M')}", size=12),
                    *dettagli,
                    ft.Divider()
                ], spacing=5),
                padding=10, bgcolor=ft.Colors.WHITE, border_radius=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK))
            )
        )
    db.close()

    content = ft.Column([
        ft.Text("Notifiche", size=30, weight=ft.FontWeight.BOLD),
        ft.Column(notifiche_list, spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    ], spacing=20, expand=True)

    return ft.View(
        route="/notifications",
        bgcolor="#1e90ff",
        controls=[
            ft.Row([
                build_menu(page),
                ft.Container(content=content, expand=True, bgcolor=ft.Colors.WHITE, padding=30, border_radius=15,
                             shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK)))
            ], expand=True)
        ]
    )