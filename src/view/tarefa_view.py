from services.tarefa_service import cadastrar_tarefa, remover_tarefa, atualizar_tarefa
import flet as ft
from connection import Session
from time import *
from model.tarefa_model import Tarefa
from functools import partial

# Função para atualizar a lista de tarefas exibida:
def atualizar_lista_tarefas(tarefas_column):
    session = Session()  # Cria uma nova sessão do banco
    try:
        tarefas_column.controls.clear()  # Limpa a interface
        todas_tarefas = session.query(Tarefa).all()  # Busca todas as tarefas

        # Armazena as referências aos checkboxes de deleção
        checkboxes_deletar = []

        for tarefa in todas_tarefas:
            # Componentes para exibir e editar uma tarefa
            descricao_textfield = ft.TextField(value=tarefa.descricao, visible=False, width=160)
            descricao_text = ft.Text(
                f"ID: {tarefa.id} - Descrição: {tarefa.descricao} - Concluída: {'Sim' if tarefa.situacao else 'Não'}"
            )
            checkbox = ft.Checkbox(value=tarefa.situacao, visible=False)

            # Botões para edição e salvamento
            c1 = ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, icon_color="Yellow")
            c2 = ft.IconButton(icon=ft.Icons.SAVE_OUTLINED, icon_color="Green", visible=False)

            # Checkbox para deleção
            checkbox_deletar = ft.Checkbox(active_color="Red", check_color="Black")

            # Adiciona a referência do checkbox_deletar à lista
            checkboxes_deletar.append((checkbox_deletar, tarefa.id))

            # Lógica ao clicar em "editar"
            def on_edit_click(tarefa, e):
                c1.visible, c2.visible = False, True
                descricao_text.visible, descricao_textfield.visible = False, True
                checkbox.visible = True
                tarefas_column.update()

            # Lógica ao clicar em "salvar"
            def on_save_click(tarefa, e):
                atualizar_tarefa(tarefa.id, descricao_textfield.value, checkbox.value)
                descricao_text.value = f"ID: {tarefa.id} - Descrição: {descricao_textfield.value} - Concluída: {'Sim' if checkbox.value else 'Não'}"
                c1.visible, c2.visible = True, False
                descricao_text.visible, descricao_textfield.visible = True, False
                checkbox.visible = False
                tarefas_column.update()

            # Callbacks de edição - WORK IN PROGRESS
            c1.on_click = partial(on_edit_click, tarefa)
            c2.on_click = partial(on_save_click, tarefa)

            # Adiciona os elementos da tarefa na interface
            tarefas_column.controls.append(
                ft.Row([checkbox_deletar, descricao_text, descricao_textfield, checkbox, c1, c2], alignment=ft.MainAxisAlignment.CENTER)
            )

        tarefas_column.update()  # Atualiza a interface
        
        # Função para deletar todas as tarefas selecionadas
        def on_delete_all_selected_click(e):
            session = Session()
            try:
                for checkbox_deletar, tarefa_id in checkboxes_deletar:
                    if checkbox_deletar.value:  # Se o checkbox estiver marcado, se estiver TRUE
                        remover_tarefa(tarefa_id)  # Deleta a tarefa
                atualizar_lista_tarefas(tarefas_column)  # Atualiza a lista após a exclusão
            finally:
                session.close()

        # Adiciona o botão "Deletar Tarefas Selecionadas" abaixo da lista
        delete_all_button = ft.ElevatedButton("Deletar Selecionadas",
                                               style=ft.ButtonStyle(text_style=ft.TextStyle(weight="BOLD")),
                                               icon=ft.Icons.DELETE,
                                               icon_color="Red",
                                               on_click=on_delete_all_selected_click,
                                               color="Red")
        
        tarefas_column.controls.append(delete_all_button)
        tarefas_column.update()

    finally:
        session.close()  # Fecha a sessão do banco


# Função para adicionar uma nova tarefa:
def on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tarefas_column):
    tarefa_cadastrada = cadastrar_tarefa(descricao_input.value, situacao_input.value)
    result_text.value = (
        f"Tarefa cadastrada com sucesso! ID: {tarefa_cadastrada.id}"
        if tarefa_cadastrada
        else "Erro ao cadastrar a tarefa."
    )
    result_text.update()
    atualizar_lista_tarefas(tarefas_column)  # Atualiza a lista de tarefas

def abrir_not(page, title, message): # Abre uma notificação de alerta - WORK IN PROGRESS
    dlg = ft.CupertinoAlertDialog(
        title=ft.Text(title, style=ft.TextStyle(weight="BOLD")),
        content=ft.Text(message, style=ft.TextStyle(font_family="Arial", size=16)),
    )
    page.open(dlg)

def toggle_tarefas(tarefas_column): # Esconde ou mostra as tarefas
    for row in tarefas_column.controls:
        row.visible = not row.visible   
        row.update()

    tarefas_column.update() 