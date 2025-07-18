import flet as ft
from datetime import date
from app.models.database import SessionLocal
from app.services.product_service import get_all_products
from app.services.damage_service import report_damage
from app.schemas.damage_schema import DamageCreate
from app.utils.menu_builder import build_menu

def damage_report_page(page: ft.Page):
    # manteniamo il font montserrat come tutte le altre pagine
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route=page.route,
            controls=[
                ft.Row([
                    build_menu(page),
                    ft.Container(
                        content=ft.Text(
                            "⛔ Utente non autorizzato",
                            size=22,
                            color=ft.Colors.RED,
                            weight=ft.FontWeight.BOLD
                        ),
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        alignment=ft.alignment.center
                    )
                ], expand=True)
            ]
        )

    # controllo permessi: solo responsabile e magazziniere possono segnalare danni
    if page.session.get("user_role") not in ["RESPONSABILE", "MAGAZZINIERE"]:
        page.go("/dashboard")
        return

    # prendo tutti i prodotti
    db = SessionLocal()
    prodotti = get_all_products(db)
    db.close()

    # preparo le opzioni per il dropdown (ID e nome così non ci sono ambiguità)
    product_options = [ft.dropdown.Option(f"{p.id} - {p.nome}") for p in prodotti]
    prodotto_dropdown = ft.Dropdown(options=product_options, width=300)

    # campo testo per descrivere il danno
    descrizione_field = ft.TextField(label="Descrizione del danno", multiline=True, width=300)

    # messaggio di conferma o errore
    message_text = ft.Text("", size=16, color="green")

    # === FUNZIONE PER SEGNALARE IL DANNO ===
    def handle_report(e):
        if not prodotto_dropdown.value:
            # controllo; almeno un prodotto va selezionato
            message_text.value = "Seleziona un prodotto."
            message_text.color = "red"
            page.update()
            return

        # prendo l'ID dal valore del dropdown (prima parte prima del trattino)
        prodotto_id = int(prodotto_dropdown.value.split(" - ")[0])

        db = SessionLocal()
        report_damage(db, DamageCreate(
            prodotto_id=prodotto_id,
            descrizione=descrizione_field.value,
            data_segnalazione=date.today()  # data di oggi, per ora va bene così
        ))
        db.close()

        message_text.value = "✅ Danno segnalato!"
        message_text.color = "green"
        page.update()

    # contenuto principale della pagina
    content = ft.Column([
        ft.Text("Segnalazione Danni", size=30, weight=ft.FontWeight.BOLD),
        prodotto_dropdown,
        descrizione_field,
        ft.ElevatedButton("Segnala Danno", on_click=handle_report, width=250),
        message_text
    ], spacing=10)

    return ft.View(
        route="/damage_report",
        bgcolor="#1e90ff",  # sfondo coerente con altre pagine gestionali
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