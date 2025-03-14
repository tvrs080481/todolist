import flet as ft
import view.tarefa_view

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # Alinhamento Vertical
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Alinhamento Horizontal
    page.window.width = 800  # Largura
    page.window.height = 400  # Altura
    page.theme_mode = ft.ThemeMode.DARK

    def handle_close(e):
        page.close(dlg_modal)
        page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to delete all those files?"),
        actions=[
            ft.TextButton("Yes", on_click=handle_close),#ft.TextButton("Yes", on_click=view.tarefa_view.on_delete_click(tarefas_column)), #'''tarefa_id''',
            ft.TextButton("No", on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: page.add(
            ft.Text("Modal dialog dismissed"),
        ),
    )


    # Campo de entrada para a descrição da tarefa
    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=300)
    
    # Campo de entrada para a situação (Checkbox)
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)
    
    # Botão para adicionar a tarefa
    add_button = ft.ElevatedButton("Cadastrar Tarefa", on_click=lambda e: view.tarefa_view.on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tarefas_column))
    
    # Área de resultado (onde será mostrado se a tarefa foi cadastrada ou não)
    result_text = ft.Text()

    # Coluna para exibir a lista de tarefas
    tarefas_column = ft.Column()

    # Adiciona todos os componentes na página
    page.add(descricao_input, situacao_input, add_button, result_text, tarefas_column)

    # Inicializa a lista de tarefas
    view.tarefa_view.atualizar_lista_tarefas(tarefas_column)

# Inicia o aplicativo Flet
ft.app(target=main)