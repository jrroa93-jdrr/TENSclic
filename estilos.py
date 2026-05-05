import flet as ft

# Paleta San Bernardo / Salud
COLOR_PRIMARIO = "#0D47A1"  # Azul Médico
COLOR_ACENTO = "#EF6C00"    # Naranja Emergencia
COLOR_FONDO = "#F5F5F5"
COLOR_TEXTO = "#212121"

# Estilos de Botón Estándar
def boton_principal(texto, icono, accion):
    return ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(icono), ft.Text(texto, weight="bold")],
            alignment="center",
        ),
        width=300,
        height=50,
        bgcolor=COLOR_PRIMARIO,
        color="white",
        on_click=accion
    )