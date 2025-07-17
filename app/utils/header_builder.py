import flet as ft

def build_header(page: ft.Page, titolo: str):
    # Header standard che usiamo in tutte le pagine
    # Mostra il titolo della pagina, l'utente loggato e il bottone di logout
    user_name = page.session.get("user_name") or "Utente"
    user_role = page.session.get("user_role") or "N/A"

    return ft.Row(
        [
            # titolo principale della pagina (espandiamo così occupa tutto lo spazio a sinistra)
            ft.Text(titolo, size=28, weight=ft.FontWeight.BOLD, expand=True),

            # nome utente e ruolo (semplice, magari in futuro aggiungiamo un avatar)
            ft.Text(f"{user_name} | {user_role}", size=14),

            # bottone di logout (rosso per renderlo ben visibile)
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
    # pulisce la sessione e torna alla pagina di login
    page.session.clear()
    page.go("/")