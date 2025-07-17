import flet as ft
from app.models.database import SessionLocal
from app.services.notification_service import get_unread_notifications

def build_menu(page: ft.Page):
    user_name = page.session.get("user_name", "Utente")
    user_role = page.session.get("user_role", "N/A")

    # ✅ Conta notifiche non lette
    db = SessionLocal()
    unread = len(get_unread_notifications(db))
    db.close()

    badge = ft.Container(
        content=ft.Text(str(unread), color=ft.Colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
        bgcolor=ft.Colors.RED,
        border_radius=10,
        padding=5,
        visible=unread > 0
    )

    buttons = [
        ft.ElevatedButton("Dashboard", on_click=lambda e: page.go("/dashboard")),
        ft.ElevatedButton("Catalogo", on_click=lambda e: page.go("/catalog")),
        ft.Row([
            ft.ElevatedButton("Notifiche", on_click=lambda e: page.go("/notifications")),
            badge
        ]),
        ft.ElevatedButton("Storico", on_click=lambda e: page.go("/history")),
    ]

    if user_role in ["RESPONSABILE", "SEGRETERIA"]:
        buttons.append(ft.ElevatedButton("Noleggi/Vendite", on_click=lambda e: page.go("/rental_sale")))
    if user_role == "RESPONSABILE":
        buttons.append(ft.ElevatedButton("Gestione Dipendenti", on_click=lambda e: page.go("/user_management")))
    if user_role in ["RESPONSABILE", "MAGAZZINIERE"]:
        buttons.append(ft.ElevatedButton("Danni", on_click=lambda e: page.go("/damage_report")))

    return ft.Container(
        content=ft.Column([
            ft.Text(user_name, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text(f"Ruolo: {user_role}", size=14, color=ft.Colors.WHITE),
            ft.Divider(height=10, color=ft.Colors.WHITE),
            *buttons
        ], spacing=10),
        bgcolor="#1e90ff",
        padding=20,
        width=200,
        border_radius=10
    )