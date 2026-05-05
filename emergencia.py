import flet as ft

def mostrar_emergencia(page):
    def llamar(numero):
        page.snack_bar = ft.SnackBar(ft.Text(f"Llamando al {numero}..."))
        page.snack_bar.open = True
        page.update()

    page.dialog = ft.AlertDialog(
        title=ft.Text("⚠️ PROTOCOLO DE EMERGENCIA"),
        content=ft.Column([
            ft.Text("Seleccione una opción de ayuda inmediata:"),
            ft.ElevatedButton("SAMU (131)", icon=ft.icons.PHONE, on_click=lambda _: llamar("131"), color="white", bgcolor="red"),
            ft.ElevatedButton("BOMBEROS (132)", icon=ft.icons.PHONE, on_click=lambda _: llamar("132"), color="white", bgcolor="red"),
            ft.Divider(),
            ft.Text("Nota: Si es electrodependiente, CGE ya tiene su prioridad.", size=12, italic=True)
        ], tight=True),
    )
    page.dialog.open = True
    page.update()