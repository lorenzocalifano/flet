import flet as ft
from app.models.database import SessionLocal
from app.services.rental_service import get_all_rentals
from app.services.sale_service import get_all_sales
from app.services.notification_service import get_unread_notifications
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header
from datetime import datetime

def dashboard_page(page: ft.Page):
    # Imposto il font unico per coerenza grafica
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    # Recupero dati dal database
    db = SessionLocal()
    noleggi = get_all_rentals(db)
    vendite = get_all_sales(db)
    notifiche_non_lette = len(get_unread_notifications(db))
    db.close()

    # Calcolo i dati del mese corrente
    oggi = datetime.now()
    anno_corrente = oggi.year
    mese_corrente = oggi.month

    noleggi_mese = len([
        n for n in noleggi
        if n.data_inizio and n.data_inizio.month == mese_corrente and n.data_inizio.year == anno_corrente
    ])

    vendite_mese = len([
        v for v in vendite
        if v.data_vendita and v.data_vendita.month == mese_corrente and v.data_vendita.year == anno_corrente
    ])

    # Funzione per creare i box di statistiche
    def stat_box(titolo, valore, colore):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(titolo, size=16, weight=ft.FontWeight.BOLD, color=colore),
                    ft.Text(str(valore), size=28, weight=ft.FontWeight.BOLD, color=colore)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=ft.Colors.with_opacity(0.05, colore),
            padding=20,
            border_radius=10,
            expand=True
        )

    # Riga con i 3 box principali: noleggi, vendite e notifiche
    stats_row = ft.Row(
        [
            stat_box("Noleggi mese", noleggi_mese, ft.Colors.BLUE),
            stat_box("Vendite mese", vendite_mese, ft.Colors.GREEN),
            stat_box("Notifiche non lette", notifiche_non_lette, ft.Colors.RED)
        ],
        spacing=15,
        expand=True
    )

    # Composizione finale della Dashboard (solo header e statistiche)
    content = ft.Column(
        [
            build_header(page, "Dashboard"),
            stats_row
        ],
        spacing=25,
        expand=True
    )

    # View finale
    return ft.View(
        route="/dashboard",
        bgcolor="#f5f5f5",
        controls=[
            ft.Row(
                [
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
                ],
                expand=True
            )
        ]
    )