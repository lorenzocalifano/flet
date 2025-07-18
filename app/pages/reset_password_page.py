import flet as ft
import random
import string
from app.models.database import SessionLocal
from app.models.user import User
from app.utils.menu_builder import build_menu
from app.utils.security import hash_password
from app.services.email_service import send_email

def reset_password_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    email_field = ft.TextField(label="Inserisci la tua email", width=300)
    message_text = ft.Text("", size=14)

    def handle_reset(e):
        db = SessionLocal()
        user = db.query(User).filter(User.email == email_field.value).first()

        if user:
            # Genera una nuova password casuale (8 caratteri)
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.password = hash_password(new_password)
            db.commit()

            # Invia email con la nuova password
            send_email(
                to_email=user.email,
                subject="Reset Password - Gestionale Magazzino",
                message=f"Ciao {user.nome},\n\nLa tua nuova password è: {new_password}\n"
                        f"Ti consigliamo di cambiarla appena possibile.\n\nGestionale Magazzino"
            )
            message_text.value = "✅ Password resettata! Controlla la tua email."
            message_text.color = "green"
        else:
            message_text.value = "❌ Email non trovata!"
            message_text.color = "red"

        db.close()
        page.update()

    content = ft.Column([
        ft.Text("Recupera Password", size=30, weight=ft.FontWeight.BOLD),
        email_field,
        ft.ElevatedButton("Resetta Password", on_click=handle_reset, width=250),
        message_text,
        ft.ElevatedButton("Torna al Login", on_click=lambda e: page.go("/"), width=250)
    ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    return ft.View(
        route="/reset_password",
        bgcolor="#1e90ff",
        controls=[
            ft.Row([
                build_menu(page),
                ft.Container(
                    content=content,
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    padding=30,
                    border_radius=15,
                    alignment=ft.alignment.center
                )
            ], expand=True)
        ]
    )