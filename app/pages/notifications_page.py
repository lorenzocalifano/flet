import flet as ft
from app.models.database import SessionLocal
from app.services.notification_service import get_all_notifications, mark_as_read

def notifications_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    def load_notifications():
        db = SessionLocal()
        notifiche = get_all_notifications(db)
        db.close()
        return notifiche

    def handle_mark_as_read(e, notification_id):
        db = SessionLocal()
        mark_as_read(db, notification_id)
        db.close()
        page.go("/notifications")  # ricarichiamo la pagina per aggiornare la lista

    notifiche = load_notifications()
    notification_list = []

    for n in notifiche:
        colore_sfondo = ft.colors.WHITE if n.letto else ft.colors.with_opacity(0.2, ft.colors.YELLOW)
        bottone = (
            ft.ElevatedButton("Segna come letta", on_click=lambda e, nid=n.id: handle_mark_as_read(e, nid))
            if n.letto == 0 else ft.Text("Già letta", color="green", size=12)
        )

        notification_list.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(f"Messaggio: {n.messaggio}", size=16, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Data: {n.data_creazione.strftime('%Y-%m-%d %H:%M:%S')}", size=14),
                            ],
                            spacing=5
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=10,
                bgcolor=colore_sfondo,
                border_radius=10,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=5,
                    color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                    offset=ft.Offset(0, 2)
                ),
                on_click=lambda e, nid=n.id: page.go(f"/notification_detail?notification_id={nid}")  # ✅ NUOVO
            )
        )

    return ft.View(
        route="/notifications",
        controls=[
            ft.AppBar(title=ft.Text("Notifiche"), center_title=True),
            ft.Column(
                [
                    ft.Text("Lista Notifiche", size=25, weight=ft.FontWeight.BOLD),
                    ft.Column(notification_list, spacing=10, scroll=ft.ScrollMode.AUTO),
                    ft.ElevatedButton("Torna alla Dashboard", on_click=lambda e: page.go("/dashboard"), width=250)
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor="#1e90ff"
    )