import flet as ft

def add_edit_product_page(page: ft.Page):
    return ft.View(
        route="/add_edit_product",
        controls=[
            ft.AppBar(title=ft.Text("Aggiungi/Modifica Prodotto"), center_title=True),
            ft.Column(
                [
                    ft.Text("Aggiungi/Modifica Prodotto", size=25, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton("Torna alla Dashboard", on_click=lambda e: page.go("/dashboard"))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
    )