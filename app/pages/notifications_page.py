import flet as ft
from app.models.database import SessionLocal
from app.services.notification_service import get_all_notifications
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header

def notifications_page(page: ft.Page):
    # Controllo Autenticazione Utente
    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route="/notifications",
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

    # Impostazioni Tema
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # Recupero Notifiche
    db = SessionLocal()
    notifiche = get_all_notifications(db)
    db.close()

    notifiche_list = []
    for n in notifiche:
        stato = "Letta" if n.letto else "Non Letta"
        color = ft.Colors.GREEN if n.letto else ft.Colors.AMBER

        notifiche_list.append(
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(n.messaggio, size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Stato: {stato}", size=12, color=color),
                        ft.Text(f"Data: {n.data_creazione.strftime('%Y-%m-%d %H:%M')}", size=12)
                    ], expand=True),
                    ft.ElevatedButton(
                        "Dettagli",
                        on_click=lambda e, nid=n.id: page.go(f"/notification_detail?notification_id={nid}")
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=15,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY),
                border_radius=8
            )
        )

    content = ft.Column([
        build_header(page, "Notifiche"),
        ft.Column(notifiche_list, spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    ], spacing=20, expand=True)

    return ft.View(
        route="/notifications",
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