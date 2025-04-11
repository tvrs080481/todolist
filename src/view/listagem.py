# view/listagem_view.py
import flet as ft
from connection import Session
from model.tarefa_model import Tarefa
from services.tarefa_service import remover_tarefa, atualizar_tarefa
session = Session()
def listagem_view(page: ft.Page):
    page.title = "Listagem de Tarefas"
    page.bgcolor = ft.colors.BLACK
    page.scroll = "auto"
    page.clean()

    def refresh():
        page.clean()
        listagem_view(page)  # Reload the page

    def create_row(tarefa):
        return ft.CupertinoContextMenu(
            enable_haptic_feedback=True,
            content=ft.Container(
                height=48,
                padding=ft.padding.symmetric(horizontal=10),
                bgcolor=ft.colors.BLACK,
                border=ft.border.all(1, ft.colors.GREY_300),
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=160,
                            alignment=ft.alignment.center_left,
                            content=ft.Text(tarefa.descricao, size=14),
                        ),
                        ft.Container(
                            width=80,
                            alignment=ft.alignment.center_left,
                            content=ft.Text("Sim" if tarefa.situacao else "Não", size=14),
                        ),
                    ]
                )
            ),
            actions=[
                ft.CupertinoContextMenuAction(
                    text=f"Editar",
                    trailing_icon=ft.Icons.EDIT,
                    on_click=lambda e: open_edit_modal(tarefa),
                ),
                ft.CupertinoContextMenuAction(
                    text=f"Remover",
                    trailing_icon=ft.Icons.DELETE,
                    is_destructive_action=True,
                    on_click=lambda e: delete_tarefa(tarefa.id),
                ),
            ],
        )

    def open_edit_modal(tarefa):
        descricao_field = ft.TextField(label="Descrição", value=tarefa.descricao)
        situacao_checkbox = ft.Checkbox(label="Concluída", value=tarefa.situacao)
        snackbar = ft.SnackBar(content=ft.Text("Tarefa atualizada com sucesso!"))


        situacao_checkbox.label = "Concluída" if tarefa.situacao else "Não Concluída"
        situacao_checkbox.value = tarefa.situacao
        situacao_checkbox.active_color = ft.colors.GREEN if tarefa.situacao else ft.colors.RED

        save_button = ft.ElevatedButton(
            "Salvar",
            icon=ft.Icons.SAVE,
            on_click=lambda e: (
                atualizar_tarefa(tarefa.id, descricao_field.value, situacao_checkbox.value),
                refresh(),
                page.close(e.control.parent),
            )
        )

        dialog = ft.AlertDialog(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        descricao_field,
                        situacao_checkbox,
                    ],
                    spacing=10,
                ),
                width=300,
            ),
            actions=[save_button]
        )

        page.open(dialog)

    def delete_tarefa(tarefa_id):
        remover_tarefa(tarefa_id)
        refresh()

    # Header
    page.add(
        ft.Container(
            height=48,
            padding=ft.padding.symmetric(horizontal=10),
            bgcolor=ft.colors.DEEP_PURPLE_400,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.colors.GREY_300)),
            content=ft.Row(
                controls=[
                    ft.Container(width=160, alignment=ft.alignment.center_left, content=ft.Text("Descrição", weight="bold")),
                    ft.Container(width=80, alignment=ft.alignment.center_left, content=ft.Text("Estado", weight="bold")),
                ]
            )
        )
    )

    # List rows
    tarefas = session.query(Tarefa).all()
    for tarefa in tarefas:
        page.add(create_row(tarefa))

    session.close()

#function to add tarefa to database
def add_tarefa(descricao, situacao):
    if situacao == True:
        situacao = 1
    else:
        situacao = 0
    nova_tarefa = Tarefa(descricao=descricao, situacao=situacao)
    session.add(nova_tarefa)
    session.commit()
    session.refresh(nova_tarefa)
    return nova_tarefa