import flet as ft

def build_header(page: ft.Page, titolo: str):
    """Header standard con titolo, utente e logout."""
    user_name = page.session.get("user_name", "Utente")
    user_role = page.session.get("user_role", "N/A")

    return ft.Row(
        [
            ft.Text(titolo, size=28, weight=ft.FontWeight.BOLD, expand=True),
            ft.Text(f"{user_name} | {user_role}", size=14, italic=True),
            ft.ElevatedButton(
                "Logout",
                on_click=lambda e: logout(page),
                style=ft.ButtonStyle(
                    padding=10,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE
                )
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

def logout(page: ft.Page):
    page.session.clear()
    page.go("/")