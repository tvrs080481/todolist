from services.tarefa_service import cadastrar_tarefa, remover_tarefa
import flet as ft
from sqlalchemy.orm import sessionmaker
from connection import Session
from time import *
from model.tarefa_model import Tarefa  # Ajuste de import, caso o seu modelo esteja em models.py

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
            tarefas_column.controls.append(
                ft.Row(
                    [
                        ft.Text(f"ID: {tarefa.id} - Descrição: {tarefa.descricao} - Concluída: {'Sim' if tarefa.situacao else 'Não'}"),
                        ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, on_click=lambda e, tarefa_id=tarefa.id: on_delete_click(tarefa_id, tarefas_column)),
                        ft.IconButton(icon=ft.Icons.DELETE_OUTLINED, on_click=lambda e, tarefa_id=tarefa.id: on_delete_click(tarefa_id, tarefas_column)),
                    ]
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