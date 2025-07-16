import flet as ft
from app.models.database import SessionLocal
from app.models.user import User
from app.services.auth_service import register_user
from app.schemas.user_schema import UserCreate, UserRole

def user_management_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

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
        value="MAGAZZINIERE", width=200
    )
    message_text = ft.Text("", size=16, color="green")

    def handle_add(e):
        if not email_field.value or not password_field.value:
            message_text.value = "Email e password obbligatorie!"
            message_text.color = "red"
            page.update()
            return
        db = SessionLocal()
        register_user(
            db,
            UserCreate(
                nome=nome_field.value,
                cognome=cognome_field.value,
                email=email_field.value,
                password=password_field.value,
                ruolo=UserRole[ruolo_dropdown.value]
            )
        )
        db.close()
        message_text.value = f"✅ Dipendente {nome_field.value} aggiunto!"
        message_text.color = "green"
        page.go("/user_management")

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
        if u.email == "mario.rossi@test.com":
            continue
        user_list.append(
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(f"{u.nome} {u.cognome}", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Email: {u.email}", size=14),
                        ft.Text(f"Ruolo: {u.ruolo.value}", size=14)
                    ]),
                    ft.Dropdown(
                        width=150,
                        value=u.ruolo.value,
                        options=[
                            ft.dropdown.Option("RESPONSABILE"),
                            ft.dropdown.Option("SEGRETERIA"),
                            ft.dropdown.Option("MAGAZZINIERE")
                        ],
                        on_change=lambda e, uid=u.id: handle_change_role(e, uid, e.control.value)
                    ),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, uid=u.id: handle_delete(e, uid))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=10, bgcolor=ft.colors.WHITE, border_radius=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.with_opacity(0.2, ft.colors.BLACK))
            )
        )

    menu_items = [
        ft.ElevatedButton("Dashboard", on_click=lambda e: page.go("/dashboard")),
        ft.ElevatedButton("Catalogo", on_click=lambda e: page.go("/catalog")),
        ft.ElevatedButton("Gestione Dipendenti", on_click=lambda e: page.go("/user_management")),
        ft.ElevatedButton("Notifiche", on_click=lambda e: page.go("/notifications"))
    ]

    content = ft.Column([
        ft.Text("Gestione Dipendenti", size=30, weight=ft.FontWeight.BOLD),
        ft.Row([nome_field, cognome_field], spacing=10),
        email_field, password_field, ruolo_dropdown,
        ft.ElevatedButton("Aggiungi Dipendente", on_click=handle_add, width=250),
        message_text, ft.Divider(),
        ft.Text("Lista Dipendenti", size=22, weight=ft.FontWeight.BOLD),
        ft.Column(user_list, spacing=10, scroll=ft.ScrollMode.AUTO)
    ], spacing=15)

    return ft.View(
        route="/user_management",
        bgcolor="#1e90ff",
        controls=[
            ft.Row([
                ft.Container(content=ft.Column(menu_items, spacing=10), width=220, bgcolor=ft.colors.BLUE_700, padding=15),
                ft.Container(content=content, expand=True, bgcolor=ft.colors.WHITE, padding=30, border_radius=15,
                             shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=ft.colors.with_opacity(0.25, ft.colors.BLACK)))
            ], expand=True)
        ]
    )