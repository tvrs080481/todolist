import flet as ft
import view.listagem
import datetime

def main(page: ft.Page):
    # --- Page setup ---
    page.title = "Cadastro de Tarefa"
    page.padding = 0                            # remove default padding
    page.bgcolor = ft.Colors.with_opacity(0.9, ft.colors.BLACK)  # make page transparent so decoration shows
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "Roboto": "fonts/Roboto/static/Roboto-VariableFont_wdth_wght.ttf",
    }

    page.theme = ft.Theme(font_family="Roboto")  # Default app font

        # --- Snackbar helper ---
    def snackbar(message, color):
        sn = ft.SnackBar(content=ft.Text(message, color=color, weight="bold"))
        page.open(sn)

    # --- Background image via decoration ---
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="../assets/menu.png",           # your asset path
            fit=ft.ImageFit.COVER,              # cover the entire page
        ),
    )

    # --- Navigation bar ---
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Home", selected_icon=ft.Icons.HOME),
            ft.NavigationBarDestination(icon=ft.Icons.LIST_OUTLINED, label="Listagem", selected_icon=ft.Icons.LIST),
        ],
        selected_index=0,
        bgcolor=ft.colors.with_opacity(0.6, ft.colors.BLACK),
        on_change=lambda e: on_nav_change(page, e),
    )

    # --- Navigation handler ---
    def on_nav_change(page, e):
        page.clean()
        if page.navigation_bar.selected_index == 0:
            main(page)
            page.go("/")
        else:
            view.listagem.listagem_view(page)
            page.go("/listagem")

    # --- Window properties ---
    page.window.center()
    page.window.width = 450
    page.window.height = 800
    page.window.full_screen = False
    page.window.resizable = False
    page.window.always_on_top = True
    page.window.icon = "../assets/icon.ico"
    page.on_error = lambda e: print("Page error:", e.data)

    #Localização
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[
            ft.Locale("pt", "pt-BR"),
        ],
        current_locale=ft.Locale("pt", "pt-BR"),
    )

    # --- Input controls ---
    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=280, border_color=ft.colors.WHITE, label_style=ft.TextStyle(color=ft.colors.WHITE), multiline=False)

    selecionada_data = {"value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
    def handle_change(e):
        selecionada_data["value"] = e.control.value.strftime('%Y-%m-%d %H:%M')
        datebutton.text = f"Data: {selecionada_data['value']}"
        datebutton.update()

    cupertino_date_picker = ft.CupertinoDatePicker(
        first_date=datetime.datetime.now(),
        last_date=datetime.datetime(2030,10,1,23,59),
        date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
        date_order=ft.CupertinoDatePickerDateOrder.DAY_MONTH_YEAR,
        on_change=handle_change,
    )
    datebutton = ft.ElevatedButton(
        f"Data: {selecionada_data['value']}",
        icon=ft.Icons.CALENDAR_MONTH,
        style=ft.ButtonStyle(text_style=ft.TextStyle(weight="bold")),
        on_click=lambda e: page.open(
            ft.CupertinoBottomSheet(
                cupertino_date_picker,
                height=216,
                padding=ft.padding.only(top=6),
            )
        ),
    )
    def on_add_click(e):
        descricao = descricao_input.value.strip()

        # Check if empty
        if not descricao:
            snackbar("A descrição não pode estar vazia.", ft.colors.RED_400)
            return

        # Check for length
        if len(descricao) > 25:
            snackbar("A descrição é muito longa. Limite de 25 caracteres.", ft.colors.RED_400)
            return

        # If all checks pass, save task
        view.listagem.add_tarefa(
            selecionada_data["value"],
            descricao,
        )

        snackbar("Tarefa cadastrada com sucesso!", ft.colors.GREEN_400)

    add_button = ft.ElevatedButton(
        "Cadastrar Tarefa",
        on_click=on_add_click,
    )

    settings_button = ft.IconButton(
        icon=ft.icons.SETTINGS_OUTLINED,
        tooltip="Configurações",
        on_click=lambda e: page.open(config_dialog),
    )

    def alterar_tema(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.icons.DARK_MODE_OUTLINED
            e.control.tooltip = 'Alterar Tema para escuro'
            page.bgcolor = ft.Colors.WHITE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.icons.LIGHT_MODE_OUTLINED
            e.control.tooltip = 'Alterar Tema para claro'
            page.bgcolor = ft.Colors.BLACK
        page.update()

    config_dialog = ft.AlertDialog(
        title=ft.Text("Configurações", weight="bold"),
        adaptive=True,
        actions=[
            ft.TextButton(
                "Fechar",
                on_click=lambda e: page.close(config_dialog),
            ),
        ],
        modal=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(icon=ft.icons.LIGHT_MODE_OUTLINED, tooltip='Alterar Tema', on_click=lambda e: alterar_tema(e)),
                    ]
                ),
                ft.Divider(),
                ft.Text("Versão do aplicativo: 1.0.0", size=14),
                ft.Text("Última atualização: 2025-16-04", size=14),
                ft.Text("Desenvolvedores: Thalita e Otávio", size=14),
            ], tight=True, spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    page.add(
    ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Row(controls=[settings_button, ft.Text("To-Do List", size=30, weight="bold", color="white")],),
                ft.Column(
                    controls=[
                        ft.Text("Gerenciador de Tarefas", size=20, weight="bold", color="white"),
                        ft.Text("Feito por: Thalita e Otávio", size=10, italic=True, color="white"),
                        ft.Divider(color="white", thickness=1),
                    ],
                    spacing=4,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),

                # Form Section
                ft.Container(
                    content=ft.Column(
                        controls=[
                            descricao_input,
                            datebutton,
                            add_button,
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor = ft.Colors(ft.colors.TRANSPARENT),
                    padding=20,
                    border_radius=10,
                    margin=ft.margin.only(top=20),
                ),
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
)