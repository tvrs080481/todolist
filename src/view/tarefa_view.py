from services.tarefa_service import cadastrar_tarefa, remover_tarefa, atualizar_tarefa
import flet as ft
from connection import Session
from time import *
from model.tarefa_model import Tarefa
from functools import partial

# Função para atualizar a lista de tarefas
def atualizar_lista_tarefas(tarefas_column):
    # Criação de uma nova sessão para pegar as tarefas
    session = Session()
    try:
        # Limpa a coluna de tarefas
        tarefas_column.controls.clear()
        
        # Busca todas as tarefas no banco de dados
        todas_tarefas = session.query(Tarefa).all()
        
        # Adiciona cada tarefa à coluna de tarefas
        for tarefa in todas_tarefas:
            checkbox_del = ft.Checkbox()
            descricao_textfield = ft.TextField(value=tarefa.descricao, visible=False)
            descricao_text = ft.Text(f"ID: {tarefa.id} - Descrição: {tarefa.descricao} - Concluída: {'Sim' if tarefa.situacao else 'Não'}")
            checkbox = ft.Checkbox(value=tarefa.situacao, visible=False)

            # Botões editar e salvar
            c1 = ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, icon_color=ft.colors.YELLOW, visible=True)
            c2 = ft.IconButton(icon=ft.Icons.SAVE_OUTLINED, icon_color=ft.colors.GREEN, visible=False)
            
            # Definir editar
            def on_edit_click(tarefa, e):
                c1.visible = False
                c2.visible = True
                descricao_text.visible = False
                descricao_textfield.visible = True
                checkbox.visible = True
                tarefas_column.update()
            
            # Definir salvar
            def on_save_click(tarefa, e):
                atualizar_tarefa(tarefa.id, descricao_textfield.value, checkbox.value)
                descricao_text.value = f"ID: {tarefa.id} - Descrição: {descricao_textfield.value} - Concluída: {'Sim' if checkbox.value else 'Não'}"
                c1.visible = True
                c2.visible = False
                descricao_text.visible = True
                descricao_textfield.visible = False
                checkbox.visible = False
                tarefas_column.update()

            c1.on_click = partial(on_edit_click, tarefa)
            c2.on_click = partial(on_save_click, tarefa)
            
            # button deletar
            c3 = ft.IconButton(icon=ft.Icons.DELETE_OUTLINED, icon_color=ft.colors.RED, on_click=lambda e, t=tarefa: on_delete_click(t.id, tarefas_column))

            # Controles
            tarefas_column.controls.append(
                ft.Row(
                    [checkbox_del, descricao_text, descricao_textfield, checkbox, c1, c2, c3]
                )
            )
        
        # Atualiza a tela com as novas tarefas
        tarefas_column.update()
    finally:
        # Fechar a sessão após o processo
        session.close()

def on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tarefas_column):
    descricao = descricao_input.value
    situacao = situacao_input.value
    
    # Chama a função de cadastro da tarefa
    tarefa_cadastrada = cadastrar_tarefa(descricao, situacao)

    if tarefa_cadastrada:
        result_text.value = f"Tarefa cadastrada com sucesso! ID: {tarefa_cadastrada.id}"
        # Atualiza a lista de tarefas na tela
        atualizar_lista_tarefas(tarefas_column)
    else:
        result_text.value = "Erro ao cadastrar a tarefa."
    
    # Atualiza o texto na tela
    result_text.update()

def on_delete_click(tarefa_id, tarefas_column, e=None):
    remover_tarefa(tarefa_id)
    atualizar_lista_tarefas(tarefas_column)