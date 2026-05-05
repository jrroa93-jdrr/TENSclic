import flet as ft
import sqlite3
from database import inicializar_db
from validaciones import validar_rut
from geolocalizacion import obtener_sectores
from mensajeria import enviar_notificacion_whatsapp, formatear_mensaje_emergencia
from api_services import llamar_emergencia, obtener_saludo_segun_hora

def main(page: ft.Page):
    # 1. Iniciamos la base de datos usando la herramienta de database.py
    inicializar_db()
    
    page.title = "TENSclic - San Bernardo"
    page.window_width = 400
    page.window_height = 800
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- NAVEGACIÓN Y VISTAS ---

    def mostrar_home():
        page.clean()
        page.floating_action_button = None 
        
        # --- USAMOS TU NUEVA API SERVICE ---
        saludo = obtener_saludo_segun_hora() 
        
        page.add(
            ft.Column(
                horizontal_alignment="center", 
                controls=[
                    ft.Container(height=40),
                    ft.Text("🏥", size=50), 
                    ft.Text("TENSclic", size=50, weight="bold", color="blue900"),
                    # Mostramos el saludo dinámico aquí
                    ft.Text(f"{saludo}, San Bernardo 2026", size=16, italic=True),
                    ft.Container(height=30),
                    ft.ElevatedButton("SOY TENS", width=300, on_click=ir_a_registro_tens),
                    ft.ElevatedButton("BUSCO CUIDADOR", width=300, on_click=ir_a_buscar_cuidador),
                    ft.ElevatedButton("REGISTRAR PACIENTE", width=300, on_click=ir_a_registro_paciente),
                    
                    # --- BOTÓN DE PÁNICO REAL ---
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "BOTÓN DE PÁNICO (SAMU)", 
                        icon="EMERGENCY",
                        bgcolor="red", 
                        color="white", 
                        on_click=lambda _: llamar_emergencia() # <--- Conectado a tu api_services
                    )
                ]
            )
        )
        page.update()

    def volver_inicio(e):
        mostrar_home()

    def ir_a_registro_tens(e):
        page.clean()
        nombre_tf = ft.TextField(label="Nombre Completo")
        rut_tf = ft.TextField(label="RUT (ej: 12.345.678-9)")
        sis_tf = ft.TextField(label="N° Registro SIS")
        especialidad_drp = ft.Dropdown(
            label="Especialidad",
            options=[
                ft.dropdown.Option("Geriatría"), 
                ft.dropdown.Option("Psiquiatría"),
                ft.dropdown.Option("Pediatría"), 
                ft.dropdown.Option("Post-Operados")
            ]
        )

        def guardar(e):
            # Aquí usamos el validador de tu archivo validaciones.py
            if not nombre_tf.value or not rut_tf.value:
                mostrar_snack("Faltan datos obligatorios", "red")
            elif not validar_rut(rut_tf.value): 
                mostrar_snack("RUT inválido", "red")
            else:
                try:
                    conn = sqlite3.connect("tensclic.db")
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO tens (nombre, rut, registro_sis, especialidad) VALUES (?,?,?,?)",
                                 (nombre_tf.value, rut_tf.value, sis_tf.value, especialidad_drp.value))
                    conn.commit()
                    conn.close()
                    mostrar_home()
                except sqlite3.IntegrityError:
                    mostrar_snack("Este RUT o SIS ya está registrado", "orange")
            page.update()

        page.add(
            ft.AppBar(title=ft.Text("Registro TENS"), bgcolor="blue"),
            ft.Column([
                nombre_tf, rut_tf, sis_tf, especialidad_drp, 
                ft.ElevatedButton("Finalizar Registro", on_click=guardar, bgcolor="green", color="white", width=400),
                ft.TextButton("Volver", on_click=volver_inicio)
            ], spacing=15)
        )

    def ir_a_registro_paciente(e):
        page.clean()
        nom_p = ft.TextField(label="Nombre Completo", icon="person")
        edad_p = ft.TextField(label="Edad", keyboard_type="number", width=180)
        dir_p = ft.TextField(label="Dirección", icon="home")
        pat_p = ft.TextField(label="Patologías", multiline=True)
        insumos = ft.Checkbox(label="¿Requiere insumos médicos?")

        def guardar_p(e):
            try:
                conn = sqlite3.connect("tensclic.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO pacientes (nombre, edad, direccion, patologias, requiere_insumos) 
                    VALUES (?,?,?,?,?)""", 
                    (nom_p.value, int(edad_p.value), dir_p.value, pat_p.value, insumos.value))
                conn.commit()
                conn.close()
                mostrar_home()
            except Exception as ex:
                mostrar_snack(f"Error: {ex}", "red")
            page.update()

        page.add(
            ft.AppBar(title=ft.Text("Nueva Ficha Clínica"), bgcolor="orange"),
            ft.Column([
                nom_p, edad_p, dir_p, pat_p, insumos,
                ft.ElevatedButton("Guardar Ficha", on_click=guardar_p, bgcolor="orange", color="white", width=400),
                ft.TextButton("Volver", on_click=volver_inicio)
            ], scroll="auto")
        )

    def ir_a_buscar_cuidador(e):
        page.clean()
        lista_cards = ft.Column(scroll="auto")
        
        def filtrar(e):
            esp = dropdown_filtro.value
            lista_cards.controls.clear()
            conn = sqlite3.connect("tensclic.db")
            cursor = conn.cursor()
            if esp == "Todos":
                cursor.execute("SELECT nombre, especialidad FROM tens")
            else:
                cursor.execute("SELECT nombre, especialidad FROM tens WHERE especialidad = ?", (esp,))
            filas = cursor.fetchall()
            conn.close()

            for f in filas:
                lista_cards.controls.append(
                    ft.Card(content=ft.Container(padding=10, content=ft.ListTile(
                        leading=ft.Icon("person", color="blue"), 
                        title=ft.Text(f[0], weight="bold"), 
                        subtitle=ft.Text(f"Especialidad: {f[1]}"))))
                )
            page.update()

        # 1. CREAMOS EL DROPDOWN SIN EL on_change ADENTRO
        dropdown_filtro = ft.Dropdown(
            label="Filtrar por especialidad",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Psiquiatría"), 
                ft.dropdown.Option("Geriatría"), 
                ft.dropdown.Option("Pediatría"), 
                ft.dropdown.Option("Post-Operados")
            ],
            width=300
        )

        # 2. ASIGNAMOS EL EVENTO EN UNA LÍNEA APARTE
        dropdown_filtro.on_change = filtrar

        page.add(
            ft.AppBar(title=ft.Text("Buscador de TENS"), bgcolor="blue"),
            ft.Column([
                dropdown_filtro, 
                ft.Divider(), 
                lista_cards, 
                ft.TextButton("Volver", on_click=volver_inicio)
            ], horizontal_alignment="center")
        )
        
        dropdown_filtro.value = "Todos"
        filtrar(None)

    # Función auxiliar para mensajes rápidos
    def mostrar_snack(texto, color):
        page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # --- ARRANQUE DE LA APP ---
    mostrar_home()

if __name__ == "__main__":
    ft.app(target=main)