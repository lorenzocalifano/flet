import flet as ft
from app.models.database import SessionLocal
from app.models.user import User
import random, string
from app.services.auth_service import hash_password

def reset_password_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    email_field = ft.TextField(label="Inserisci la tua email", width=300)
    message_text = ft.Text("", size=16, color="green")

    def handle_reset(e):
        db = SessionLocal()
        utente = db.query(User).filter(User.email == email_field.value.strip()).first()
        if not utente:
            message_text.value = "❌ Nessun utente trovato con questa email."
            message_text.color = "red"
        else:
            nuova_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            utente.password = hash_password(nuova_password)
            db.commit()
            message_text.value = f"✅ Password resettata! Nuova password temporanea: {nuova_password}"
            message_text.color = "green"
        db.close()
        page.update()

    return ft.View(
        route="/reset_password",
        bgcolor="#1e90ff",  # ✅ Sfondo pieno come login
        controls=[
            ft.Container(
                expand=True,  # ✅ Riempie tutto lo sfondo
                bgcolor="#1e90ff",
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Recupera Password", size=25, weight=ft.FontWeight.BOLD),
                                    email_field,
                                    ft.ElevatedButton("Resetta Password", on_click=handle_reset, width=250),
                                    message_text,
                                    ft.ElevatedButton("Torna al Login", on_click=lambda e: page.go("/"), width=250)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
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
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )