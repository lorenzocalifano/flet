import flet as ft
from app.models.database import SessionLocal
from app.services.notification_service import get_all_notifications
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header

def notifications_page(page: ft.Page):
    # solito font montserrat, per coerenza con tutto il gestionale
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route="/notifications",
            bgcolor="#f5f5f5",
            controls=[ft.Row([ft.Text("Utente non autorizzato", size=22, color="red", weight=ft.FontWeight.BOLD)],
                             alignment=ft.MainAxisAlignment.CENTER)]
        )

    # prendo tutte le notifiche
    db = SessionLocal()
    notifiche = get_all_notifications(db)
    db.close()

    notifiche_list = []
    for n in notifiche:
        # decido colore e testo in base allo stato
        stato = "✅ Letta" if n.letto else "🔔 Non letta"
        color = ft.Colors.GREEN if n.letto else ft.Colors.AMBER

        # aggiungo la card della singola notifica
        notifiche_list.append(
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        # messaggio principale
                        ft.Text(n.messaggio, size=16, weight=ft.FontWeight.BOLD),
                        # stato (colorato, giusto per farlo risaltare)
                        ft.Text(f"Stato: {stato}", size=12, color=color),
                        # data di creazione (per ora solo Y-M-D e ora, va bene così)
                        ft.Text(f"Data: {n.data_creazione.strftime('%Y-%m-%d %H:%M')}", size=12)
                    ], expand=True),
                    # bottone per andare nel dettaglio (così non affolliamo la lista)
                    ft.ElevatedButton(
                        "Dettagli",
                        on_click=lambda e, nid=n.id: page.go(f"/notification_detail?notification_id={nid}")
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=15,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY),  # grigino leggero, tanto per staccare
                border_radius=8
            )
        )

    # colonna scrollabile, altrimenti con tante notifiche diventa ingestibile
    content = ft.Column([
        build_header(page, "Notifiche"),
        ft.Column(notifiche_list, spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    ], spacing=20, expand=True)

    return ft.View(
        route="/notifications",
        bgcolor="#f5f5f5",  # grigio chiaro per differenziarla dalle altre
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