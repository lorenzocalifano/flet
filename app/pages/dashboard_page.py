import flet as ft
from app.models.database import SessionLocal
from app.services.product_service import get_all_products
from app.services.rental_service import get_all_rentals
from app.services.sale_service import get_all_sales
from app.services.notification_service import get_unread_notifications
from app.models.user import User
from collections import Counter
from flet.plotly_chart import PlotlyChart
import plotly.graph_objects as go
from datetime import datetime

def dashboard_page(page: ft.Page):
    page.theme = ft.Theme(font_family="Montserrat")
    page.update()

    db = SessionLocal()
    prodotti = get_all_products(db)
    noleggi = get_all_rentals(db)
    vendite = get_all_sales(db)
    notifiche = get_unread_notifications(db)
    utenti = db.query(User).all()
    db.close()

    user_name = page.session.get("user_name") or "Utente"
    user_role = page.session.get("user_role") or "MAGAZZINIERE"

    # ✅ MENU LATERALE
    menu_items = [
        ft.Text(f"{user_name}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ft.Text(f"Ruolo: {user_role}", size=14, color=ft.colors.WHITE),
        ft.Divider(height=10, color=ft.colors.WHITE),
        ft.ElevatedButton("Dashboard", on_click=lambda e: page.go("/dashboard")),
        ft.ElevatedButton("Catalogo", on_click=lambda e: page.go("/catalog")),
    ]
    if user_role in ["RESPONSABILE", "SEGRETERIA"]:
        menu_items.append(ft.ElevatedButton("Storico", on_click=lambda e: page.go("/history")))
        menu_items.append(ft.ElevatedButton("Noleggi/Vendite", on_click=lambda e: page.go("/rental_sale")))
    if user_role == "RESPONSABILE":
        menu_items.append(ft.ElevatedButton("Gestione Dipendenti", on_click=lambda e: page.go("/user_management")))
    if user_role in ["RESPONSABILE", "MAGAZZINIERE"]:
        menu_items.append(ft.ElevatedButton("Danni", on_click=lambda e: page.go("/damage_report")))
    menu_items.append(ft.ElevatedButton("Notifiche", on_click=lambda e: page.go("/notifications")))

    # ✅ GRAFICO A BARRE
    prodotti_nomi = []
    noleggi_quantita = []
    vendite_quantita = []
    for p in prodotti:
        n_q = sum(n.quantita for n in noleggi if n.prodotto_id == p.id)
        v_q = sum(v.quantita for v in vendite if v.prodotto_id == p.id)
        if n_q > 0 or v_q > 0:
            prodotti_nomi.append(p.nome)
            noleggi_quantita.append(n_q)
            vendite_quantita.append(v_q)
    grafico_barre = PlotlyChart(
        go.Figure(
            data=[
                go.Bar(name="Noleggi", x=prodotti_nomi, y=noleggi_quantita, marker=dict(color="blue")),
                go.Bar(name="Vendite", x=prodotti_nomi, y=vendite_quantita, marker=dict(color="green"))
            ]
        ).update_layout(barmode="group", title="Noleggi e Vendite per Prodotto", height=400)
    )

    # ✅ GRAFICO A TORTA
    ruoli = [u.ruolo.value for u in utenti]
    conteggio_ruoli = Counter(ruoli)
    grafico_torta = PlotlyChart(
        go.Figure(
            data=[go.Pie(labels=list(conteggio_ruoli.keys()), values=list(conteggio_ruoli.values()), hole=0.4)]
        ).update_layout(title="Distribuzione Ruoli Dipendenti", height=400)
    )

    # ✅ GRAFICO A LINEE (noleggi e vendite per mese)
    def group_by_month(operazioni, field):
        counter = Counter([getattr(o, field).strftime("%Y-%m") for o in operazioni])
        mesi = sorted(counter.keys())
        valori = [counter[m] for m in mesi]
        return mesi, valori

    mesi_n, valori_n = group_by_month(noleggi, "data_inizio")
    mesi_v, valori_v = group_by_month(vendite, "data_vendita")
    mesi = sorted(set(mesi_n) | set(mesi_v))

    valori_n_all = [valori_n[mesi_n.index(m)] if m in mesi_n else 0 for m in mesi]
    valori_v_all = [valori_v[mesi_v.index(m)] if m in mesi_v else 0 for m in mesi]

    grafico_linee = PlotlyChart(
        go.Figure(
            data=[
                go.Scatter(x=mesi, y=valori_n_all, mode="lines+markers", name="Noleggi", line=dict(color="blue")),
                go.Scatter(x=mesi, y=valori_v_all, mode="lines+markers", name="Vendite", line=dict(color="green"))
            ]
        ).update_layout(title="Andamento Mensile Noleggi e Vendite", xaxis_title="Mese", yaxis_title="Operazioni", height=400)
    )

    # ✅ CONTENUTO PRINCIPALE
    content = ft.Column([
        ft.Text("Dashboard", size=35, weight=ft.FontWeight.BOLD),
        ft.Row([
            ft.Container(content=ft.Column([
                ft.Text("Prodotti in magazzino", size=18),
                ft.Text(str(len(prodotti)), size=28, weight=ft.FontWeight.BOLD)
            ]), width=250, height=120, padding=15, bgcolor=ft.colors.BLUE_100, border_radius=10),
            ft.Container(content=ft.Column([
                ft.Text("Noleggi totali", size=18),
                ft.Text(str(len(noleggi)), size=28, weight=ft.FontWeight.BOLD)
            ]), width=250, height=120, padding=15, bgcolor=ft.colors.GREEN_100, border_radius=10),
            ft.Container(content=ft.Column([
                ft.Text("Notifiche non lette", size=18),
                ft.Text(str(len(notifiche)), size=28, weight=ft.FontWeight.BOLD)
            ]), width=250, height=120, padding=15, bgcolor=ft.colors.AMBER_100, border_radius=10)
        ], spacing=30),
        ft.Row([grafico_barre, grafico_torta], spacing=30),
        grafico_linee
    ], spacing=30, scroll=ft.ScrollMode.AUTO)

    return ft.View(
        route="/dashboard",
        bgcolor="#1e90ff",
        controls=[
            ft.Row([
                ft.Container(content=ft.Column(menu_items, spacing=10), width=220, bgcolor=ft.colors.BLUE_700, padding=15),
                ft.Container(content=content, expand=True, bgcolor=ft.colors.WHITE, padding=30, border_radius=15,
                             shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=ft.colors.with_opacity(0.25, ft.colors.BLACK)))
            ], expand=True)
        ]
    )