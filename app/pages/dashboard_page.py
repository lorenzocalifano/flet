import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import get_all_products
from app.services.rental_service import get_all_rentals
from app.services.notification_service import get_unread_notifications

def dashboard_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    db = SessionLocal()
    prodotti = get_all_products(db)
    noleggi = get_all_rentals(db)
    notifiche = get_unread_notifications(db)
    db.close()

    user_name = page.session.get("user_name") or "Utente"
    user_role = page.session.get("user_role") or "MAGAZZINIERE"

    # ✅ Menu laterale (stile desktop)
    menu_items = [
        ft.Text(f"{user_name}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ft.Text(f"Ruolo: {user_role}", size=14, color=ft.colors.WHITE),
        ft.Divider(height=10, color=ft.colors.WHITE),
        ft.ElevatedButton("Dashboard", on_click=lambda e: page.go("/dashboard")),
        ft.ElevatedButton("Catalogo", on_click=lambda e: page.go("/catalog")),
    ]

    if user_role in ["RESPONSABILE", "SEGRETERIA"]:
        menu_items.append(ft.ElevatedButton("Storico", on_click=lambda e: page.go("/history")))
        menu_items.append(ft.ElevatedButton("Noleggi/Vendite", on_click=lambda e: page.go("/rental_sale")))

    if user_role == "RESPONSABILE":
        menu_items.append(ft.ElevatedButton("Gestione Dipendenti", on_click=lambda e: page.go("/user_management")))

    if user_role in ["RESPONSABILE", "MAGAZZINIERE"]:
        menu_items.append(ft.ElevatedButton("Danni", on_click=lambda e: page.go("/damage_report")))

    menu_items.append(ft.ElevatedButton("Notifiche", on_click=lambda e: page.go("/notifications")))

    # ✅ Contenuto principale (occupiamo tutto lo spazio 16:9)
    content = ft.Column(
        [
            ft.Text("Dashboard", size=35, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Prodotti in magazzino", size=18),
                        ft.Text(str(len(prodotti)), size=28, weight=ft.FontWeight.BOLD)
                    ]),
                    width=250, height=120,
                    padding=15, bgcolor=ft.colors.BLUE_100, border_radius=10
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Noleggi totali", size=18),
                        ft.Text(str(len(noleggi)), size=28, weight=ft.FontWeight.BOLD)
                    ]),
                    width=250, height=120,
                    padding=15, bgcolor=ft.colors.GREEN_100, border_radius=10
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Notifiche non lette", size=18),
                        ft.Text(str(len(notifiche)), size=28, weight=ft.FontWeight.BOLD)
                    ]),
                    width=250, height=120,
                    padding=15, bgcolor=ft.colors.AMBER_100, border_radius=10
                )
            ], spacing=30)
        ],
        spacing=30,
        scroll=ft.ScrollMode.AUTO
    )

    return ft.View(
        route="/dashboard",
        bgcolor="#1e90ff",
        controls=[
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column(menu_items, spacing=10),
                        width=220,
                        bgcolor=ft.colors.BLUE_700,
                        padding=15
                    ),
                    ft.Container(
                        content=content,
                        expand=True,
                        bgcolor=ft.colors.WHITE,
                        padding=30,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=8,
                            color=ft.colors.with_opacity(0.25, ft.colors.BLACK),
                            offset=ft.Offset(0, 4)
                        )
                    )
                ],
                expand=True
            )
        ]
    )