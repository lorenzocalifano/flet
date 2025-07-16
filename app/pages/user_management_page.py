import flet as ft
from app.models.database import SessionLocal
from app.models.user import User
from app.services.auth_service import register_user
from app.schemas.user_schema import UserCreate, UserRole

def user_management_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # ✅ SOLO RESPONSABILE
    if page.session.get("user_role") != "RESPONSABILE":
        page.go("/dashboard")
        return

    db = SessionLocal()
    utenti = db.query(User).all()
    db.close()

    nome_field = ft.TextField(label="Nome", width=200)
    cognome_field = ft.TextField(label="Cognome", width=200)
    email_field = ft.TextField(label="Email", width=200)
    password_field = ft.TextField(label="Password", password=True, width=200)
    ruolo_dropdown = ft.Dropdown(
        label="Ruolo",
        options=[
            ft.dropdown.Option("RESPONSABILE"),
            ft.dropdown.Option("SEGRETERIA"),
            ft.dropdown.Option("MAGAZZINIERE")
        ],
        value="MAGAZZINIERE",
        width=200
    )
    message_text = ft.Text("", size=16, color="green")

    def handle_add(e):
        if not email_field.value or not password_field.value:
            message_text.value = "Email e password sono obbligatorie!"
            page.update()
            return
        db = SessionLocal()
        try:
            nuovo_utente = register_user(
                db,
                UserCreate(
                    nome=nome_field.value,
                    cognome=cognome_field.value,
                    email=email_field.value,
                    password=password_field.value,
                    ruolo=UserRole[ruolo_dropdown.value]
                )
            )
            message_text.value = f"✅ Dipendente {nuovo_utente.nome} {nuovo_utente.cognome} aggiunto!"
        except Exception as ex:
            message_text.value = f"Errore: {str(ex)}"
        finally:
            db.close()
            page.go("/user_management")  # ricarica la pagina

    def handle_delete(e, user_id):
        db = SessionLocal()
        db.query(User).filter(User.id == user_id).delete()
        db.commit()
        db.close()
        page.go("/user_management")

    def handle_change_role(e, user_id, new_role):
        db = SessionLocal()
        utente = db.query(User).filter(User.id == user_id).first()
        if utente:
            utente.ruolo = UserRole[new_role]
            db.commit()
        db.close()
        page.go("/user_management")

    user_list = []
    for u in utenti:
        if u.email == "mario.rossi@test.com":  # ✅ Non permettiamo di eliminare l'utente principale
            continue
        user_list.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(f"{u.nome} {u.cognome}", size=16, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Email: {u.email}", size=14),
                                ft.Text(f"Ruolo: {u.ruolo.value}", size=14),
                            ],
                            spacing=3
                        ),
                        ft.Dropdown(
                            width=150,
                            value=u.ruolo.value,
                            options=[
                                ft.dropdown.Option("RESPONSABILE"),
                                ft.dropdown.Option("SEGRETERIA"),
                                ft.dropdown.Option("MAGAZZINIERE")
                            ],
                            on_change=lambda e, user_id=u.id: handle_change_role(e, user_id, e.control.value)
                        ),
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, uid=u.id: handle_delete(e, uid))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=10,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=5,
                    color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                    offset=ft.Offset(0, 2)
                )
            )
        )

    return ft.View(
        route="/user_management",
        controls=[
            ft.AppBar(title=ft.Text("Gestione Dipendenti"), center_title=True),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Aggiungi Dipendente", size=25, weight=ft.FontWeight.BOLD),
                        ft.Row([nome_field, cognome_field], spacing=10),
                        email_field,
                        password_field,
                        ruolo_dropdown,
                        ft.ElevatedButton("Aggiungi", on_click=handle_add, width=200),
                        message_text,
                        ft.Divider(),
                        ft.Text("Lista Dipendenti", size=22, weight=ft.FontWeight.BOLD),
                        ft.Column(user_list, spacing=10, scroll=ft.ScrollMode.AUTO),
                        ft.ElevatedButton("Torna alla Dashboard", on_click=lambda e: page.go("/dashboard"), width=250)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                alignment=ft.alignment.top_center,
                padding=30,
                width=500,
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
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor="#1e90ff"
    )