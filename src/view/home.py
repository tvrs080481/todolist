import flet as ft
import view.tarefa_view
import time

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # Alinhamento Vertical
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Alinhamento Horizontal
    page.window.width = 450  # Largura
    page.window.height = 800  # Altura
    page.window.full_screen = False # Janela não é fullscreen
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = True
    page.auto_scroll = True # Janela scrollable
    page.window.resizable = False  # Janela não redimensionável
    page.window.always_on_top = True  # Janela fica sempre no topo

    # Centralizar janela
    page.window.center()

    # Definir ícone da janela
    page.window.icon = "C:\\Users\\ead\\Documents\\SENAI_SESI\\OTAVIO\\fork\\todolist\\src\\assets\\icon.ico"

    # Campo de entrada para a descrição da tarefa
    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=280)
    
    # Campo de entrada para a situação (Checkbox)
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)

    # Botão para esconder/mostrar tarefas
    toggle_button = ft.ElevatedButton("Mostrar Tarefas", on_click=lambda e: view.tarefa_view.toggle_tarefas(tarefas_column))
    
    # Botão para adicionar a tarefa
    add_button = ft.ElevatedButton("Cadastrar Tarefa", on_click=lambda e: view.tarefa_view.on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tarefas_column))
    
    # Área de resultado (onde será mostrado se a tarefa foi cadastrada ou não)
    result_text = ft.Text()

    # Coluna para exibir a lista de tarefas
    tarefas_column = ft.Column()

    # Adiciona todos os componentes na página
    page.add(descricao_input, situacao_input, add_button, result_text, tarefas_column, toggle_button)

    # Inicializa a lista de tarefas
    view.tarefa_view.atualizar_lista_tarefas(tarefas_column)

    def tutorial():
        view.tarefa_view.abrir_not(page, "Tutorial", "Vou te ensinar como utilizar o To-Do List!")
        time.sleep(5)
        view.tarefa_view.abrir_not(page, "Tutorial", "1. Digite a descrição da tarefa no campo de texto.")
        time.sleep(5)
        view.tarefa_view.abrir_not(page, "Tutorial", "2. Marque a caixa de seleção se a tarefa estiver concluída.")
        time.sleep(5)
        view.tarefa_view.abrir_not(page, "Tutorial", "3. Clique no botão 'Cadastrar Tarefa' para adicionar a tarefa.")
        time.sleep(5)
        view.tarefa_view.abrir_not(page, "Tutorial", "4. Para editar uma tarefa, clique no ícone de lápis.")
        time.sleep(5)
        view.tarefa_view.abrir_not(page, "Tutorial", "5. Para salvar sua edição, clique no ícone do disquete.")
        time.sleep(5)
        view.tarefa_view.abrir_not(page, "Tutorial", "6. Para excluir uma tarefa, selecione quais quer deletar e aperte o botão de deletar-las.")
        time.sleep(5)
        view.tarefa_view.abrir_not(page, "Tutorial", "7. Pronto! Agora você já sabe como usar o To-Do List.")
        