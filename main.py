import flet as ft
import principal as pr

# Función principal
def main(page: ft.Page):

    def ingresar(e: ft.ControlEvent):
        page.clean()
        pr.main(page)

    # Configuración de la página
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.title = "Inicio de sesión"
    page.window.width  = 800
    page.window.height = 600

    # Componentes de la página
    logo = ft.Icon("person", size=100, color="pink")
    txt_bienvenido = ft.Text("Bienvenida", size=30)
    txt_usuario = ft.TextField(label="Username/correo", width=250)
    txt_contra  = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250)
    btn_login   = ft.FilledButton(
        "Iniciar sesión",
        icon=ft.Icons.LOGIN,
        width=250,
        color="white",
        bgcolor="pink",
        on_click=ingresar
    )
    page.add(logo, txt_bienvenido, txt_usuario, txt_contra, btn_login)
    # Actualizar la página
    page.update()


# Inicio de la aplicación
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
