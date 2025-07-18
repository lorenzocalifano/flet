import flet as ft
from app.models.database import SessionLocal
from app.services.auth_service import register_user  # solo se usiamo reset reale, altrimenti non serve
from app.utils.menu_builder import build_menu

def reset_password_page(page: ft.Page):
    # Tema coerente con il resto dell'app
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    email_field = ft.TextField(label="Inserisci la tua email", width=300)
    message_text = ft.Text("", size=14, color="red")

    def handle_reset(e):
        if not email_field.value:
            message_text.value = "Inserisci un'email valida."
            message_text.color = "red"
        else:
            # Qui possiamo mettere logica reale di reset (email finta)
            message_text.value = f"Se esiste un account per {email_field.value}, riceverai istruzioni per il reset."
            message_text.color = "green"
        page.update()

    # Contenuto centrale allineato come la pagina di login
    content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Recupera Password", size=30, weight=ft.FontWeight.BOLD),
                email_field,
                ft.ElevatedButton("Resetta Password", on_click=handle_reset, width=250),
                message_text,
                ft.ElevatedButton("Torna al Login", on_click=lambda e: page.go("/"), width=250)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        alignment=ft.alignment.center,
        padding=30,
        width=400,
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )

    return ft.View(
        route="/reset_password",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor="#1e90ff",
        controls=[content]
    )