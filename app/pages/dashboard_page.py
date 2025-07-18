import os
import flet as ft
import plotly.graph_objects as go
from flet.plotly_chart import PlotlyChart
from app.models.database import SessionLocal
from app.services.rental_service import get_all_rentals
from app.services.sale_service import get_all_sales
from app.services.notification_service import get_unread_notifications
from app.utils.menu_builder import build_menu
from app.utils.header_builder import build_header
from collections import Counter
from datetime import datetime

def dashboard_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    if page.session.get("user_name") == "Utente" or page.session.get("user_role") == "N/A":
        return ft.View(
            route="/dashboard",
            bgcolor="#f5f5f5",
            controls=[ft.Row([ft.Text("Utente non autorizzato", size=22, color="red", weight=ft.FontWeight.BOLD)],
                             alignment=ft.MainAxisAlignment.CENTER)]
        )

    # Dati DB
    db = SessionLocal()
    noleggi = get_all_rentals(db)
    vendite = get_all_sales(db)
    notifiche_non_lette = len(get_unread_notifications(db))
    db.close()

    mese_corrente = datetime.now().month
    noleggi_mese = len([n for n in noleggi if n.data_inizio.month == mese_corrente])
    vendite_mese = len([v for v in vendite if v.data_vendita.month == mese_corrente])

    # Statistiche
    def stat_box(titolo, valore, colore):
        return ft.Container(
            content=ft.Column([
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

    stats_row = ft.Row([
        stat_box("Noleggi mese", noleggi_mese, ft.Colors.BLUE),
        stat_box("Vendite mese", vendite_mese, ft.Colors.GREEN),
        stat_box("Notifiche non lette", notifiche_non_lette, ft.Colors.RED)
    ], spacing=15, expand=True)

    # Su docker SOLO BOX
    if os.getenv("DOCKER") == "1":
        content = ft.Column([
            build_header(page, "Dashboard"),
            stats_row
        ], spacing=25, expand=True)

        return ft.View(
            route="/dashboard",
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

    # Se non siamo su docker: GRAFICI
    # --- Andamento Mensile ---
    mesi_noleggi = {}
    mesi_vendite = {}
    for n in noleggi:
        m = n.data_inizio.strftime("%b")
        mesi_noleggi[m] = mesi_noleggi.get(m, 0) + 1
    for v in vendite:
        m = v.data_vendita.strftime("%b")
        mesi_vendite[m] = mesi_vendite.get(m, 0) + 1

    mesi = sorted(set(mesi_noleggi.keys()) | set(mesi_vendite.keys()),
                  key=lambda x: datetime.strptime(x, "%b").month)

    andamento_fig = go.Figure()
    andamento_fig.add_trace(go.Scatter(
        x=mesi,
        y=[mesi_noleggi.get(m, 0) for m in mesi],
        mode="lines+markers",
        name="Noleggi",
        line=dict(color="blue")
    ))
    andamento_fig.add_trace(go.Scatter(
        x=mesi,
        y=[mesi_vendite.get(m, 0) for m in mesi],
        mode="lines+markers",
        name="Vendite",
        line=dict(color="green")
    ))
    andamento_fig.update_layout(
        title=dict(text="Andamento Mensile",
                   font=dict(family="Montserrat", size=22, color="black"), x=0.5),
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor="white"
    )
    andamento_chart = PlotlyChart(andamento_fig, expand=True)

    # --- Top Prodotti ---
    prodotti_noleggiati = Counter([n.prodotto_id for n in noleggi])
    top_prodotti = prodotti_noleggiati.most_common(5)
    if top_prodotti:
        prodotti = [str(pid) for pid, _ in top_prodotti]
        valori = [q for _, q in top_prodotti]
    else:
        prodotti, valori = [], []

    top_fig = go.Figure()
    top_fig.add_trace(go.Bar(
        x=prodotti,
        y=valori,
        marker_color="orange",
        name="Top Noleggi"
    ))
    top_fig.update_layout(
        title=dict(text="Top 5 Prodotti Noleggiati",
                   font=dict(family="Montserrat", size=22, color="black"), x=0.5),
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor="white"
    )
    top_chart = PlotlyChart(top_fig, expand=True)

    grafici_row = ft.Row([andamento_chart, top_chart], spacing=15, expand=True)

    content = ft.Column([
        build_header(page, "Dashboard"),
        stats_row,
        grafici_row
    ], spacing=25, expand=True)

    return ft.View(
        route="/dashboard",
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