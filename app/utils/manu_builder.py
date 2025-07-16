import flet as ft

def build_menu(page):
    user_role = page.session.get("user_role") or "MAGAZZINIERE"
    user_name = page.session.get("user_name") or "Utente"

    menu_items = [
        ft.Text(f"{user_name}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ft.Text(f"Ruolo: {user_role}", size=14, color=ft.colors.WHITE),
        ft.Divider(height=10, color=ft.colors.WHITE),
        ft.ElevatedButton("Dashboard", on_click=lambda e: page.go("/dashboard")),
        ft.ElevatedButton("Catalogo", on_click=lambda e: page.go("/catalog")),
        ft.ElevatedButton("Notifiche", on_click=lambda e: page.go("/notifications"))
    ]

    if user_role in ["RESPONSABILE", "SEGRETERIA"]:
        menu_items.append(ft.ElevatedButton("Storico", on_click=lambda e: page.go("/history")))
        menu_items.append(ft.ElevatedButton("Noleggi/Vendite", on_click=lambda e: page.go("/rental_sale")))

    if user_role == "RESPONSABILE":
        menu_items.append(ft.ElevatedButton("Gestione Dipendenti", on_click=lambda e: page.go("/user_management")))

    if user_role in ["RESPONSABILE", "MAGAZZINIERE"]:
        menu_items.append(ft.ElevatedButton("Danni", on_click=lambda e: page.go("/damage_report")))

    return ft.Container(content=ft.Column(menu_items, spacing=10), width=220, bgcolor=ft.colors.BLUE_700, padding=15)