import flet as ft
from connection import Session
from model.tarefa_model import Tarefa
from datetime import datetime
from services.tarefa_service import remover_tarefa, atualizar_tarefa, cadastrar_tarefa

session = Session()

def listagem_view(page: ft.Page):
    page.title = "Listagem de Tarefas"
    page.bgcolor = ft.colors.BLACK
    page.scroll = "auto"
    page.clean()
    page.padding = 0
    page.bgcolor = ft.Colors.with_opacity(0.9, ft.colors.BLACK)
    page.theme_mode = ft.ThemeMode.DARK
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="../assets/menu.png",
            fit=ft.ImageFit.COVER,
        ),
    )

    selected_tasks = {}

    def refresh():
        listagem_view(page)


    def open_edit_modal(tarefa):
        descricao_field = ft.TextField(label="Descrição", value=tarefa.descricao)
        selecionada_data = {"value": datetime.now().strftime('%Y-%m-%d %H:%M')}

        def handle_change(e):
            selecionada_data["value"] = e.control.value.strftime('%Y-%m-%d %H:%M')
            datebutton.text = f"Data: {selecionada_data['value']}"
            datebutton.update()

        cupertino_date_picker = ft.CupertinoDatePicker(
            first_date=datetime.now(),
            last_date=datetime(2030, 10, 1, 23, 59),
            date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
            on_change=handle_change,
        )

        datebutton = ft.ElevatedButton(
            f"Data: {selecionada_data['value']}",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(
                ft.CupertinoBottomSheet(
                    cupertino_date_picker,
                    height=216,
                    padding=ft.padding.only(top=6),
                )
            ),
        )

        save_button = ft.ElevatedButton(
            "Salvar",
            icon=ft.Icons.SAVE,
            on_click=lambda e: (
                atualizar_tarefa(tarefa.id, descricao_field.value),
                refresh(),
                page.close(dialog),
            )
        )

        dialog = ft.AlertDialog(
            title=ft.Text("Editar Tarefa"),
            content=ft.Column(
                [
                    descricao_field,
                    datebutton,
                    ft.Row(
                        [
                            save_button,
                            ft.ElevatedButton(
                                "Cancelar",
                                icon=ft.Icons.CANCEL,
                                on_click=lambda e: page.close(dialog),
                            ),
                        ]
                    ),
                ]
            ),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: page.close(dialog)),
            ],
        )

        page.open(dialog)

    def delete_tarefa(tarefa_id):
        remover_tarefa(tarefa_id)
        refresh()

    def update_selection(tarefa_id, is_selected):
        selected_tasks[tarefa_id] = is_selected

    def delete_selected_tasks(e):
        for tarefa_id, is_selected in selected_tasks.items():
            if is_selected:
                remover_tarefa(tarefa_id)
        refresh()

    expansion_panel_list = ft.ExpansionPanelList(
        expand_icon_color=ft.colors.WHITE,
        elevation=4,
        divider_color=ft.colors.WHITE,
    )

    tarefas = session.query(Tarefa).all()

    for tarefa in tarefas:
        selected_tasks[tarefa.id] = False

        checkbox = ft.Checkbox(
            value=selected_tasks[tarefa.id],
            check_color=ft.colors.RED,
            active_color=ft.colors.RED,
            on_change=lambda e, tid=tarefa.id: update_selection(tid, e.control.value),
        )

        panel = ft.ExpansionPanel(
            header=ft.ListTile(
                leading=checkbox,
                title=ft.Text(tarefa.descricao),
                subtitle=ft.Text(f"Data: {tarefa.data.strftime('%Y-%m-%d %H:%M')}", weight="bold"),
            ),

            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Ações disponíveis:", weight="bold"),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda e, t=tarefa: open_edit_modal(t),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED_500,
                                tooltip="Remover",
                                on_click=lambda e, tid=tarefa.id: delete_tarefa(tid),
                            ),
                        ]
                    ),
                ]
            )
        )

        expansion_panel_list.controls.append(panel)

    delete_selected_button = ft.ElevatedButton(
        text="Excluir Selecionadas",
        icon=ft.icons.DELETE,
        icon_color=ft.colors.RED,
        style=ft.ButtonStyle(text_style=ft.TextStyle(weight="bold")),
        color=ft.colors.RED,
        bgcolor=ft.colors.BLACK,
        visible = True if len(selected_tasks) > 0 else False,
        on_click=lambda e: (
            delete_selected_tasks(e),
            refresh(),
        ),
    )

    page.add(
        ft.Container(
            padding=ft.padding.all(10),
            content=ft.Column(
                controls=[
                    delete_selected_button,
                    expansion_panel_list
                ]
            )
        )
    )

    session.close()

def add_tarefa(data, descricao):
    cadastrar_tarefa(data, descricao)
