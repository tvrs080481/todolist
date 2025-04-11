'''
Definir funções para gerenciar tarefas no banco de dados. - Otávio
'''
from model.tarefa_model import Tarefa
from sqlalchemy.exc import SQLAlchemyError
from connection import Session

# Cadastrar uma nova tarefa
def cadastrar_tarefa(descricao: str, situacao: bool):
    try:
        nova_tarefa = Tarefa(descricao=descricao, situacao=situacao)  # Cria uma tarefa
        session = Session()
        session.add(nova_tarefa)  # Adiciona à sessão
        session.commit()  # Salva no banco
        session.refresh(nova_tarefa)  # Atualiza o objeto
        return nova_tarefa  # Retorna a nova tarefa
    except SQLAlchemyError as e:
        session.rollback()  # Reverte mudançasit c em caso de erro
        print(f"Erro ao cadastrar tarefa: {e}")
        return None
    finally:
        session.close()  # Fecha a sessão

# Remover uma tarefa pelo ID
def remover_tarefa(id: int):
    session = Session()
    try:
        tarefa = session.query(Tarefa).filter(Tarefa.id == id).first()  # Busca a tarefa
        if tarefa:
            session.delete(tarefa)  # Remove do banco
            session.commit()  # Confirma a exclusão
            return True
        else:
            print(f"Tarefa com ID {id} não encontrada.")
            return False
    except Exception as e:
        session.rollback()  # Reverte mudanças em caso de erro
        print(f"Erro deletando tarefa: {e}")
        return False
    finally:
        session.close()  # Fecha a sessão

# Atualizar uma tarefa pelo ID
def atualizar_tarefa(tarefa_id: int, descricao: str, situacao: int):
    session = Session()
    try:
        tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()  # Busca a tarefa
        if tarefa:
            tarefa.descricao = descricao  # Atualiza a descrição
            tarefa.situacao = situacao  # Atualiza a situação
            session.commit()  # Salva alterações
            session.refresh(tarefa)  # Atualiza o objeto
            return tarefa  # Retorna a tarefa atualizada
        else:
            print(f"Tarefa com ID {tarefa_id} não encontrada.")
            return None
    except Exception as e:
        session.rollback()  # Reverte mudanças em caso de erro
        print(f"Erro atualizando tarefa: {e}")
        return None
    finally:
        session.close()  # Fecha a sessão