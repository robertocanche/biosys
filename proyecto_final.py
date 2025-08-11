import flet as ft
from pyairtable import Api
from pyairtable.formulas import match

# Configuración de Airtable
API_KEY = "patFExIrSAwNvNAtv.feb16e3a6d8f28a983ad46e2748f86ca74450d71df293eceab2a6c2713aa4dbb"
BASE_ID = "app5uJBTnU59OVxCl"
TABLE_NAME_USUARIO = "Usuario"
# Nombre de la tabla para bioenergias, usada para consultar
TABLE_NAME_BIOENERGIA = "Bioenergias" 

api = Api(API_KEY)
tabla_usuarios = api.base(BASE_ID).table(TABLE_NAME_USUARIO)
tabla_bioenergias = api.base(BASE_ID).table(TABLE_NAME_BIOENERGIA)

def main(page: ft.Page):
    page.title = "Sistema de Gestión"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.window.width = 800
    page.window.height = 600
    
    # Snackbar para mensajes
    mensaje_snack = ft.SnackBar(content=ft.Text(""))
    def mostrar_snack(texto):
        mensaje_snack.content.value = texto
        mensaje_snack.open = True
        page.snack_bar = mensaje_snack
        page.update()

    # ---- Vistas ----

    # Vista de inicio de sesión
    usuario_input = ft.TextField(label="Usuario")
    password_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    
    def validar_credenciales(e):
        usuario = usuario_input.value
        password = password_input.value
        if not usuario or not password:
            mostrar_snack("Por favor, ingrese usuario y contraseña.")
            return

        try:
            formula = match({"clave": usuario, "contra": password})
            registro = tabla_usuarios.first(formula=formula)
            if registro:
                page.go("/menu")
            else:
                mostrar_snack("Usuario o contraseña incorrectos.")
        except Exception as err:
            print(f"Error de Airtable: {err}")
            mostrar_snack("Error de conexión con Airtable.")

    def view_login():
        return ft.View(
            route="/",
            controls=[
                ft.AppBar(title=ft.Text("Iniciar sesión")),
                usuario_input,
                password_input,
                ft.ElevatedButton("Ingresar", on_click=validar_credenciales),
                ft.TextButton("¿No tienes cuenta? Regístrate aquí", on_click=lambda e: page.go("/agregar_usuario"))
            ]
        )
    
    # Vista del menú principal (con el nuevo botón)
    def view_menu():
        return ft.View(
            route="/menu",
            controls=[
                ft.AppBar(title=ft.Text("Menú principal")),
                ft.Column(
                    controls=[
                        ft.ElevatedButton("Agregar nuevo usuario", on_click=lambda e: page.go("/agregar_usuario")),
                        ft.ElevatedButton("Consultar usuarios", on_click=lambda e: page.go("/consultar_usuarios")),
                        # Nuevo botón que lleva a la vista de biomasa
                        ft.ElevatedButton("Consultar bioenergías", on_click=lambda e: page.go("/biomasa")),
                        ft.ElevatedButton("Cerrar sesión", on_click=lambda e: page.go("/"))
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ]
        )

    # Vista para agregar usuario
    def view_agregar_usuario():
        nombre_field = ft.TextField(label="Nombre")
        clave_field = ft.TextField(label="Usuario (clave)")
        contra_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)

        def registrar_usuario_interno(e):
            if not nombre_field.value or not clave_field.value or not contra_field.value:
                mostrar_snack("Todos los campos son obligatorios.")
                return

            try:
                tabla_usuarios.create({
                    "nombre": nombre_field.value,
                    "clave": clave_field.value,
                    "contra": contra_field.value
                })
                mostrar_snack("Usuario registrado correctamente.")
                nombre_field.value = ""
                clave_field.value = ""
                contra_field.value = ""
                page.update()
            except Exception as err:
                print("Error al registrar:", err)
                mostrar_snack(f"Error al registrar: {err}")

        return ft.View(
            route="/agregar_usuario",
            controls=[
                ft.AppBar(title=ft.Text("Agregar nuevo usuario")),
                nombre_field,
                clave_field,
                contra_field,
                ft.ElevatedButton("Registrar", on_click=registrar_usuario_interno),
                ft.ElevatedButton("Volver", on_click=lambda e: page.go("/menu"))
            ]
        )
    
    # Vista para consultar usuarios
    def view_consultar_usuarios():
        try:
            registros = tabla_usuarios.all()
            filas = []
            for r in registros:
                data = r.get("fields", {})
                filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(data.get("nombre", ""))),
                            ft.DataCell(ft.Text(data.get("clave", ""))),
                            ft.DataCell(ft.Text(data.get("contra", "")))
                        ]
                    )
                )
            tabla = ft.DataTable(
                columns=[
                    ft.DataColumn(label=ft.Text("Nombre")),
                    ft.DataColumn(label=ft.Text("Usuario")),
                    ft.DataColumn(label=ft.Text("Contraseña"))
                ],
                rows=filas
            )
            
            return ft.View(
                route="/consultar_usuarios",
                controls=[
                    ft.AppBar(title=ft.Text("Usuarios registrados")),
                    tabla,
                    ft.ElevatedButton("Volver", on_click=lambda e: page.go("/menu"))
                ]
            )
        except Exception as err:
            print("Error al consultar:", err)
            mostrar_snack("Error al obtener datos de Airtable.")
            return view_menu()

    # Nueva vista para biomasa, basada en el código que proporcionaste
    def view_biomasa():
        txt_cultivoorigen = ft.Text("Cultivo Origen", size=20)
        txt_parteaprovechada = ft.Text("Parte Aprovechada", size=20)

        productos = ["Caña de azúcar", "Cacao", "Maíz", "Coco", "Plátano"]
        partes_aprovechadas = ["Hoja", "Tallo", "Cáscara", "Bagazo", "Rastrojo"]

        productos_dropdown = ft.Dropdown(
            label="Selecciona un cultivo de origen",
            options=[
                ft.dropdown.Option(producto) for producto in productos
            ],
            width=250,
        )

        partes_aprovechadas_dropdown = ft.Dropdown(
            label="Selecciona una parte aprovechada", # Corregido el label
            options=[
                ft.dropdown.Option(parteaprovechada) for parteaprovechada in partes_aprovechadas
            ],
            width=250,
        )

        txt_cantidad = ft.TextField(label="cantidad (ton)", width=250)
        txt_humedad = ft.TextField(label="humedad %", width=250)
        txt_Acultivada = ft.TextField(label="area cultivada", width=250)
        txt_contenergetico = ft.TextField(label="contenido energetico", width=250)
        txt_municipio = ft.TextField(label="municipios", width=250)
        
        # Botón para volver al menú principal
        btn_volver = ft.ElevatedButton("Volver", on_click=lambda e: page.go("/menu"))

        return ft.View(
            route="/biomasa",
            controls=[
                ft.AppBar(title=ft.Text("Consulta de Biomasa")),
                ft.Column(
                    controls=[
                        txt_cultivoorigen,
                        productos_dropdown,
                        txt_parteaprovechada,
                        partes_aprovechadas_dropdown,
                        txt_cantidad,
                        txt_humedad,
                        txt_Acultivada,
                        txt_contenergetico,
                        txt_municipio,
                        btn_volver
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ]
        )
    
    # ---- Manejo de rutas ----
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(view_login())
        elif page.route == "/menu":
            page.views.append(view_menu())
        elif page.route == "/agregar_usuario":
            page.views.append(view_agregar_usuario())
        elif page.route == "/consultar_usuarios":
            page.views.append(view_consultar_usuarios())
        # Maneja la nueva ruta de biomasa
        elif page.route == "/biomasa":
            page.views.append(view_biomasa())
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

# Inicia la aplicación con la función principal
ft.app(target=main)

