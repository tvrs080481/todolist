from services.tarefa_service import cadastrar_tarefa, remover_tarefa, atualizar_tarefa
import flet as ft
from connection import Session
from time import *
from model.tarefa_model import Tarefa
from functools import partial # Importar função partial de ordem superior

# Este código gerencia uma aplicação para cadastro, listagem, edição e remoção de tarefas usando Flet.

# Função para atualizar a lista de tarefas exibida:
def atualizar_lista_tarefas(tarefas_column):
    session = Session()  # Cria uma nova sessão do banco
    try:
        tarefas_column.controls.clear()  # Limpa a interface
        todas_tarefas = session.query(Tarefa).all()  # Busca todas as tarefas

        for tarefa in todas_tarefas:
            # Componentes para exibir e editar uma tarefa
            descricao_textfield = ft.TextField(value=tarefa.descricao, visible=False)
            descricao_text = ft.Text(
                f"ID: {tarefa.id} - Descrição: {tarefa.descricao} - Concluída: {'Sim' if tarefa.situacao else 'Não'}"
            )
            checkbox = ft.Checkbox(value=tarefa.situacao, visible=False)

            # Botões para edição e salvamento
            c1 = ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, icon_color=ft.colors.YELLOW)
            c2 = ft.IconButton(icon=ft.Icons.SAVE_OUTLINED, icon_color=ft.colors.GREEN, visible=False)

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

            c1.on_click = partial(on_edit_click, tarefa)
            c2.on_click = partial(on_save_click, tarefa)

            # Botão de exclusão
            c3 = ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINED,
                icon_color=ft.colors.RED,
                on_click=lambda e, t=tarefa: on_delete_click(t.id, tarefas_column),
            )

            # Adiciona os elementos da tarefa na interface
            tarefas_column.controls.append(
                ft.Row([descricao_text, descricao_textfield, checkbox, c1, c2, c3])
            )

        tarefas_column.update()  # Atualiza a interface
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

# Função para deletar uma tarefa:
def on_delete_click(tarefa_id, tarefas_column, e=None):
    remover_tarefa(tarefa_id)  # Remove a tarefa do banco
    atualizar_lista_tarefas(tarefas_column)  # Atualiza a interface