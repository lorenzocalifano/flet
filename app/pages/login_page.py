import flet as ft
from app.models.database import SessionLocal
from app.services.auth_service import authenticate_user

def login_page(page: ft.Page):
    # Imposta font globale Montserrat
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    email_field = ft.TextField(label="Email", width=300)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    message_text = ft.Text("", color="red")

    def handle_login(e):
        db = SessionLocal()
        user = authenticate_user(db, email_field.value, password_field.value)
        db.close()

        if user:
            page.session.set("user_id", user.id)
            page.session.set("user_name", f"{user.nome} {user.cognome}")
            page.session.set("user_role", user.ruolo.value.upper())

            # Massimizza veramente a schermo intero
            page.window_maximized = True
            page.window_full_screen = True

            page.go("/dashboard")

            page.go("/dashboard")
        else:
            message_text.value = "Credenziali errate, riprova."
        page.update()

    return ft.View(
        route="/",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Accedi al Gestionale", size=30, weight=ft.FontWeight.BOLD),
                        email_field,
                        password_field,
                        ft.ElevatedButton("Login", on_click=handle_login, width=150),
                        message_text,
                        ft.TextButton("Password dimenticata?", on_click=lambda e: page.go("/reset_password"))
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                alignment=ft.alignment.center,
                padding=30,
                width=400,
                bgcolor=ft.colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=8,
                    color=ft.colors.with_opacity(0.25, ft.colors.BLACK),
                    offset=ft.Offset(0, 4)
                )
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor="#1e90ff"  # Sfondo blu personalizzato
    )