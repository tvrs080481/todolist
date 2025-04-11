import flet as ft
import view.listagem
import datetime

def main(page: ft.Page):
    # Set page properties
    page.title = "Cadastro de Tarefa"
    page.add(ft.SafeArea(ft.Text("To-Do List", size=30, weight="bold")))
    page.add(ft.SafeArea(ft.Text("Gerenciador de Tarefas", size=20, weight="bold", color="White")))  # Title
    page.add(ft.SafeArea(ft.Text("Feito por: Thalita e Otávio", size=10, italic=True, color="White")))  # Subtitle
    divider = ft.SafeArea(ft.Divider(color="White", thickness=1))  # Divider for better UI
    page.add(divider)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Ensure this is an enum
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Ensure this is an enum
    page.window.width = 450

    page.window.height = 800
    page.bgcolor = "Black"
    page.scroll = True
    page.auto_scroll = True
    page.window.full_screen = False
    page.theme_mode = ft.ThemeMode.DARK
    page.window.resizable = False
    page.window.always_on_top = True

    def snackbar(message):
        ft.SnackBarTheme.bgcolor = ft.Colors.BLACK
        sn = ft.SnackBar(content=ft.Text(message))
        page.open(sn)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Home", selected_icon=ft.Icons.HOME),
            ft.NavigationBarDestination(icon=ft.Icons.LIST_OUTLINED, label="Listagem", selected_icon=ft.Icons.LIST),
        ],
        on_change=lambda e: on_nav_change(e),
        selected_index=0,
    )

    def on_nav_change(e):
        if page.navigation_bar.selected_index == 0:
            page.clean()
            main(page)
            page.go("/")
        elif page.navigation_bar.selected_index == 1:
            page.clean()
            view.listagem.listagem_view(page)
            page.go("/listagem")

    # Center the window
    page.window.center()

    # Set the window icon
    page.window.icon = "../assets/icon.ico"

    # Declare elements
    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=280)
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)
    result_text = ft.Text()

    # Variable to store the selected date
    selecionada_data = {"value": None}

    def handle_change(e):
        # Update the selected date
        selecionada_data["value"] = e.control.value.strftime('%Y-%m-%d %H:%M')
        # Update the result_text element
        snackbar(f"Data selecionada: {selecionada_data['value']}")
        result_text.update()

    cupertino_date_picker = ft.CupertinoDatePicker(
        first_date=datetime.datetime.now(),
        date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
        last_date=datetime.datetime(year=2030, month=10, day=1, hour=23, minute=59),
        on_change=handle_change,
    )

    datebutton = ft.ElevatedButton(
        "Data",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.CupertinoBottomSheet(
                cupertino_date_picker,
                height=216,
                padding=ft.padding.only(top=6),
            )
        ),
    )

    add_button = ft.ElevatedButton(
        "Cadastrar Tarefa",
        on_click=lambda e: view.listagem.add_tarefa(
            #selecionada_data["value"],
            descricao_input.value,
            situacao_input,
        ),
    )

    # Layout container
    container_content = ft.Column(
        controls=[
            descricao_input,
            datebutton,
            situacao_input,
            add_button,
            result_text,
        ],
        spacing=10
    )

    container = ft.Container(
        content=container_content,
        expand=True,
        adaptive=True,
        width=400,
        padding=20,
        border_radius=10,
        margin=ft.margin.only(top=10),
    )

    page.add(container)