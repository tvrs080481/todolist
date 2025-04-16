import flet as ft
from model.tarefa_model import Tarefa
from datetime import datetime, timedelta
from services.tarefa_service import remover_tarefa, atualizar_tarefa, cadastrar_tarefa, query_tarefa

def listagem_view(page: ft.Page):
    page.title = "Listagem de Tarefas "
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

    def color_priority(tarefa):
        if tarefa.data <= datetime.now():
            return 0  # Red - most urgent
        elif tarefa.data <= datetime.now() + timedelta(days=1):
            return 1  # Yellow - soon
        return 2  # Transparent - not urgent

    def refresh():
        listagem_view(page)
    
    def snackbar(message):
        sn = ft.SnackBar(content=ft.Text(message, weight="bold"), behavior="floating")
        page.open(sn)
    
    def check_tarefa_expiration(tarefa):
        if tarefa.data <= datetime.now():
            return ft.colors.RED_500
        elif tarefa.data <= datetime.now() + timedelta(days=1):
            return ft.colors.YELLOW_500
        return ft.colors.TRANSPARENT
    
    def change_text_color_based_on_expiration(tarefa):
        if tarefa.data <= datetime.now():
            return ft.colors.BLACK
        elif tarefa.data <= datetime.now() + timedelta(days=1):
            return ft.colors.BLACK
        return ft.colors.WHITE

    def open_edit_modal(tarefa):
        descricao_field = ft.TextField(label="Descrição", value=tarefa.descricao, border_color=ft.colors.WHITE)
        descricao_field.autofocus = True
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
        )

        save_button = ft.TextButton(
            "Salvar",
            icon=ft.Icons.SAVE,
            on_click=lambda e: (
            atualizar_tarefa(tarefa.id, descricao_field.value),
            refresh(),
            page.close(dialog),
            ),
        )

        dialog = ft.AlertDialog(
            title=ft.Text("Editar Tarefa", color=ft.colors.WHITE),
            content=ft.Column(
            [
                ft.Divider(thickness=1, color=ft.colors.WHITE),
                descricao_field,
                datebutton,
            ],
            tight=True,
            ),
            adaptive=True,
            modal=True,
            content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
            actions=[
            save_button,
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
        elevation=4,
    )

    tarefas = sorted(query_tarefa(), key=lambda t: (color_priority(t), t.data))

    for tarefa in tarefas:
        selected_tasks[tarefa.id] = False

        checkbox = ft.Checkbox(
            value=selected_tasks[tarefa.id],
            fill_color=ft.colors.WHITE,
            on_change=lambda e, tid=tarefa.id: update_selection(tid, e.control.value),
            border_side=ft.BorderSide(width=2, color= ft.colors.BLACK),
        )

        expansion_panel_list.divider_color = change_text_color_based_on_expiration(tarefa)
        expansion_panel_list.expanded_icon_color = change_text_color_based_on_expiration(tarefa)


        panel = ft.ExpansionPanel(
            bgcolor=check_tarefa_expiration(tarefa),
            header=ft.CupertinoContextMenu(
            enable_haptic_feedback=True,
            content=ft.ListTile(
                leading=checkbox,
                title=ft.Text(tarefa.descricao, weight="bold", style=ft.TextStyle(color=change_text_color_based_on_expiration(tarefa))),
                bgcolor=check_tarefa_expiration(tarefa),
            ),
            actions=[
                ft.CupertinoContextMenuAction(
                text="Editar",
                trailing_icon=ft.Icons.EDIT,
                on_click=lambda e, t=tarefa: open_edit_modal(t),
                ),
                ft.CupertinoContextMenuAction(
                text="Completar",
                is_destructive_action=True,
                trailing_icon=ft.Icons.CHECK,
                on_click=lambda e, tid=tarefa.id: delete_tarefa(tid),
                ),
            ],
            ),
            content=ft.Column(
            controls=[
                ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.cupertino_icons.ALARM,
                        icon_color=change_text_color_based_on_expiration(tarefa),
                        disabled=True,
                    ),
                    ft.Text(f"Data: {tarefa.data.strftime('%Y-%m-%d %H:%M')}", weight="bold", height=20, color=change_text_color_based_on_expiration(tarefa)),
                ]
                ),
            ]
            ),
        )

        expansion_panel_list.controls.append(panel)

    delete_selected_button = ft.ElevatedButton(
        text="Completar Selecionadas",
        icon=ft.icons.CHECK,
        style=ft.ButtonStyle(text_style=ft.TextStyle(weight="bold")),
        bgcolor=ft.colors.TRANSPARENT,
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
    def checar_tarefas_e_notificar():
        tarefas = query_tarefa()
        tarefas_atrasadas = [tarefa.descricao for tarefa in tarefas if tarefa.data <= datetime.now()]
        tarefas_proximas = [tarefa.descricao for tarefa in tarefas if datetime.now() < tarefa.data <= datetime.now() + timedelta(days=1)]

        if tarefas_atrasadas:
            snackbar(f"Você tem tarefas atrasadas: {', '.join(tarefas_atrasadas)}")
        if tarefas_proximas:
            snackbar(f"Cuidado! Tarefas próximas do vencimento: {', '.join(tarefas_proximas)}")
        
    checar_tarefas_e_notificar()

def add_tarefa(data, descricao):
    cadastrar_tarefa(data, descricao)
