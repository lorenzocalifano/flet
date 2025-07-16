import flet as ft
from app.models.database import SessionLocal
from app.services.notification_service import get_all_notifications

def notifications_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    db = SessionLocal()
    notifiche = get_all_notifications(db)
    db.close()

    menu_items = [
        ft.ElevatedButton("Dashboard", on_click=lambda e: page.go("/dashboard")),
        ft.ElevatedButton("Catalogo", on_click=lambda e: page.go("/catalog")),
        ft.ElevatedButton("Notifiche", on_click=lambda e: page.go("/notifications"))
    ]
    if page.session.get("user_role") in ["RESPONSABILE", "SEGRETERIA"]:
        menu_items.append(ft.ElevatedButton("Storico", on_click=lambda e: page.go("/history")))
        menu_items.append(ft.ElevatedButton("Noleggi/Vendite", on_click=lambda e: page.go("/rental_sale")))
    if page.session.get("user_role") == "RESPONSABILE":
        menu_items.append(ft.ElevatedButton("Gestione Dipendenti", on_click=lambda e: page.go("/user_management")))
    if page.session.get("user_role") in ["RESPONSABILE", "MAGAZZINIERE"]:
        menu_items.append(ft.ElevatedButton("Danni", on_click=lambda e: page.go("/damage_report")))

    notifiche_list = []
    for n in notifiche:
        stato = "Letta" if n.letto else "Non letta"
        color = ft.colors.GREEN if n.letto else ft.colors.AMBER
        notifiche_list.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Column([
                            ft.Text(n.messaggio, size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Stato: {stato}", size=14, color=color),
                            ft.Text(f"Data: {n.data_creazione.strftime('%Y-%m-%d %H:%M:%S')}", size=12)
                        ]),
                        ft.ElevatedButton("Dettagli", on_click=lambda e, nid=n.id: page.go(f"/notification_detail?notification_id={nid}"))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=10, bgcolor=ft.colors.WHITE, border_radius=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.with_opacity(0.2, ft.colors.BLACK))
            )
        )

    content = ft.Column([
        ft.Text("Notifiche", size=30, weight=ft.FontWeight.BOLD),
        ft.Column(notifiche_list, spacing=10, scroll=ft.ScrollMode.AUTO)
    ], spacing=20)

    return ft.View(
        route="/notifications",
        bgcolor="#1e90ff",
        controls=[
            ft.Row([
                ft.Container(content=ft.Column(menu_items, spacing=10), width=220, bgcolor=ft.colors.BLUE_700, padding=15),
                ft.Container(content=content, expand=True, bgcolor=ft.colors.WHITE, padding=30, border_radius=15,
                             shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=ft.colors.with_opacity(0.25, ft.colors.BLACK)))
            ], expand=True)
        ]
    )