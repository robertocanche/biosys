import flet as ft

def main(page: ft.Page):

    def mostrar_registro(e: ft.ControlEvent):
        page.clean()
        
        
    # Configuración de la página
    page.title = "Menú principal"
    page.theme_mode = "light"
    page.appbar = ft.AppBar(
        title=ft.Text("Sistema de Gestión de Bioenergías"),
        leading=ft.Icon("energy_savings_leaf"),
        color="white",
        bgcolor="purple"
    )
    # Componentes de la página
    btn_registro = ft.ElevatedButton("Registro", on_click=mostrar_registro)
    btn_consultas = ft.ElevatedButton("Consulta")
    # Añadir a la página
    page.add(btn_registro,btn_consultas)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)