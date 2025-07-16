import flet as ft
from urllib.parse import parse_qs
from app.models.database import SessionLocal
from app.services.notification_service import get_all_notifications, mark_as_read
from app.services.rental_service import get_all_rentals
from app.services.sale_service import get_all_sales
from app.services.product_service import get_product_by_id

def notification_detail_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # ✅ Recupero ID notifica in sicurezza
    query_params = parse_qs(page.route.split("?")[1]) if "?" in page.route else {}
    notification_id = int(query_params.get("notification_id", [0])[0])

    db = SessionLocal()
    notifiche = get_all_notifications(db)
    notifica = next((n for n in notifiche if n.id == notification_id), None)

    operazione_dettagli = []
    if notifica:
        try:
            if notifica.tipo == "noleggio" and notifica.operazione_id:
                noleggio = next((n for n in get_all_rentals(db) if n.id == notifica.operazione_id), None)
                if noleggio:
                    prodotto = get_product_by_id(db, noleggio.prodotto_id)
                    operazione_dettagli = [
                        ft.Text("Tipo Operazione: NOLEGGIO", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Prodotto: {prodotto.nome if prodotto else '-'}", size=16),
                        ft.Text(f"Cliente: {noleggio.cliente}", size=16),
                        ft.Text(f"Quantità: {noleggio.quantita}", size=16),
                        ft.Text(f"Data Inizio: {noleggio.data_inizio}", size=16),
                        ft.Text(f"Data Fine: {noleggio.data_fine}", size=16),
                        ft.Text(f"Metodo Pagamento: {noleggio.metodo_pagamento}", size=16),
                        ft.Text(f"Stato: {noleggio.stato}", size=16)
                    ]
            elif notifica.tipo == "vendita" and notifica.operazione_id:
                vendita = next((v for v in get_all_sales(db) if v.id == notifica.operazione_id), None)
                if vendita:
                    prodotto = get_product_by_id(db, vendita.prodotto_id)
                    operazione_dettagli = [
                        ft.Text("Tipo Operazione: VENDITA", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Prodotto: {prodotto.nome if prodotto else '-'}", size=16),
                        ft.Text(f"Cliente: {vendita.cliente}", size=16),
                        ft.Text(f"Quantità: {vendita.quantita}", size=16),
                        ft.Text(f"Data Vendita: {vendita.data_vendita}", size=16),
                        ft.Text(f"Metodo Pagamento: {vendita.metodo_pagamento}", size=16),
                        ft.Text(f"Stato: {vendita.stato}", size=16)
                    ]
        except Exception as e:
            operazione_dettagli = [ft.Text(f"Impossibile caricare i dettagli: {str(e)}", color="red")]

    db.close()

    if not notifica:
        return ft.View(
            route="/notification_detail",
            controls=[
                ft.Text("Notifica non trovata", color="red", size=20),
                ft.ElevatedButton("Torna alle Notifiche", on_click=lambda e: page.go("/notifications"))
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor="#1e90ff"
        )

    stato = "Letta" if notifica.letto else "Non letta"

    def handle_mark_as_read(e):
        if not notifica.letto:
            db = SessionLocal()
            mark_as_read(db, notifica.id)
            db.close()
            page.go(f"/notification_detail?notification_id={notification_id}")

    return ft.View(
        route="/notification_detail",
        controls=[
            ft.AppBar(title=ft.Text("Dettagli Notifica"), center_title=True),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Dettagli Notifica", size=25, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Messaggio: {notifica.messaggio}", size=18),
                        ft.Text(f"Data: {notifica.data_creazione.strftime('%Y-%m-%d %H:%M:%S')}", size=18),
                        ft.Text(f"Stato: {stato}", size=18),
                        ft.Divider(),
                        *(operazione_dettagli if operazione_dettagli else [ft.Text("Nessun dettaglio aggiuntivo", size=16)]),
                        ft.Divider(),
                        ft.ElevatedButton(
                            "Segna come letta",
                            on_click=handle_mark_as_read,
                            disabled=not notifica.letto == 0,
                            width=250
                        ),
                        ft.ElevatedButton(
                            "Torna alle Notifiche",
                            on_click=lambda e: page.go("/notifications"),
                            width=250)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                alignment=ft.alignment.center,
                padding=30,
                width=400,
                bgcolor=ft.colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=8,
                    color=ft.colors.with_opacity(0.25, ft.colors.BLACK),
                    offset=ft.Offset(0, 4)
                )
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor="#1e90ff"
    )