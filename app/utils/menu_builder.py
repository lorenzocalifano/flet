import flet as ft

def build_menu(page):
    user_role = page.session.get("user_role") or "MAGAZZINIERE"
    user_name = page.session.get("user_name") or "Utente"

    def menu_button(text, icon, route):
        return ft.ElevatedButton(
            text,
            icon=icon,
            on_click=lambda e: page.go(route),
            style=ft.ButtonStyle(
                overlay_color=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

    menu_items = [
        ft.Text(f"👤 {user_name}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ft.Text(f"Ruolo: {user_role}", size=14, color=ft.colors.WHITE),
        ft.Divider(height=10, color=ft.colors.WHITE),
        menu_button("Dashboard", ft.icons.DASHBOARD, "/dashboard"),
        menu_button("Catalogo", ft.icons.INVENTORY, "/catalog"),
        menu_button("Notifiche", ft.icons.NOTIFICATIONS, "/notifications")
    ]

    if user_role in ["RESPONSABILE", "SEGRETERIA"]:
        menu_items.append(menu_button("Storico", ft.icons.HISTORY, "/history"))
        menu_items.append(menu_button("Noleggi/Vendite", ft.icons.SWAP_HORIZ, "/rental_sale"))

    if user_role == "RESPONSABILE":
        menu_items.append(menu_button("Gestione Dipendenti", ft.icons.GROUP, "/user_management"))

    if user_role in ["RESPONSABILE", "MAGAZZINIERE"]:
        menu_items.append(menu_button("Danni", ft.icons.REPORT, "/damage_report"))

    return ft.Container(
        content=ft.Column(menu_items, spacing=10),
        width=220,
        bgcolor=ft.colors.BLUE_700,
        padding=15,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.colors.with_opacity(0.25, ft.colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )