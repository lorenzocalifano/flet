import flet as ft
from app.models.database import SessionLocal
from app.services.user_service import get_all_users, delete_user, update_user_role, create_user
from app.schemas.user_schema import UserCreate, UserRole
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header

def user_management_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    if page.session.get("user_role") != "RESPONSABILE":
        page.go("/dashboard")
        return

    db = SessionLocal()
    utenti = get_all_users(db)
    db.close()

    nome_field = ft.TextField(label="Nome", width=200)
    cognome_field = ft.TextField(label="Cognome", width=200)
    email_field = ft.TextField(label="Email", width=200)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=200)
    ruolo_dropdown = ft.Dropdown(
        label="Ruolo",
        options=[ft.dropdown.Option(r.name) for r in UserRole],
        width=200
    )
    message_text = ft.Text("", size=14, color="green")

    user_list_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh_list():
        db = SessionLocal()
        utenti = get_all_users(db)
        db.close()
        user_list_column.controls.clear()

        for u in utenti:
            role_dropdown = ft.Dropdown(
                value=u.ruolo.name,
                options=[ft.dropdown.Option(r.name) for r in UserRole],
                width=150,
                on_change=lambda e, uid=u.id: update_role(uid, e.control.value)
            )
            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color=ft.Colors.RED,
                on_click=lambda e, uid=u.id: handle_delete(uid)
            )
            user_list_column.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(f"{u.nome} {u.cognome}", size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Email: {u.email}", size=12, italic=True)
                        ], expand=True),
                        role_dropdown,
                        delete_btn
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY),
                    border_radius=8
                )
            )
        page.update()

    def handle_add(e):
        if not nome_field.value or not cognome_field.value or not email_field.value or not password_field.value or not ruolo_dropdown.value:
            message_text.value = "⚠️ Tutti i campi sono obbligatori!"
            message_text.color = "red"
        else:
            db = SessionLocal()
            try:
                create_user(db, UserCreate(
                    nome=nome_field.value,
                    cognome=cognome_field.value,
                    email=email_field.value,
                    password=password_field.value,
                    ruolo=UserRole[ruolo_dropdown.value]
                ))
                message_text.value = f"✅ Dipendente {nome_field.value} aggiunto!"
                message_text.color = "green"
                refresh_list()
            except Exception as ex:
                message_text.value = f"❌ Errore: {str(ex)}"
                message_text.color = "red"
            finally:
                db.close()
        page.update()

    def handle_delete(user_id):
        db = SessionLocal()
        try:
            delete_user(db, user_id)
            refresh_list()
        finally:
            db.close()

    def update_role(user_id, new_role):
        db = SessionLocal()
        try:
            update_user_role(db, user_id, UserRole[new_role])
            refresh_list()
        finally:
            db.close()

    refresh_list()

    content = ft.Column([
        build_header(page, "Gestione Dipendenti"),
        ft.Row([nome_field, cognome_field, email_field, password_field, ruolo_dropdown],
               alignment=ft.MainAxisAlignment.START, spacing=10),
        ft.ElevatedButton("Aggiungi Dipendente", on_click=handle_add),
        message_text,
        ft.Text("Lista Dipendenti", size=20, weight=ft.FontWeight.BOLD),
        user_list_column
    ], spacing=15, expand=True)

    return ft.View(
        route="/user_management",
        bgcolor="#f5f5f5",
        controls=[
            ft.Row([
                build_menu(page),
                ft.Container(
                    content=content,
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    padding=30,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK)
                    )
                )
            ], expand=True)
        ]
    )