from model.tarefa_model import Tarefa
from sqlalchemy.exc import SQLAlchemyError
from connection import Session


def cadastrar_tarefa(descricao: str, situacao: bool):
    try:
        # Criar uma nova instância do modelo Tarefa com os dados fornecidos
        nova_tarefa = Tarefa(descricao=descricao, situacao=situacao)
        session = Session()
        # Adicionar a tarefa na sessão
        session.add(nova_tarefa)
        
        # Commit para salvar a tarefa no banco de dados
        session.commit()
        
        #Refresh a sessão
        session.refresh(nova_tarefa)

        # Retorna o objeto Tarefa inserido
        return nova_tarefa

    except SQLAlchemyError as e:
        # Caso ocorra um erro, faz o rollback
        session.rollback()
        print(f"Erro ao cadastrar tarefa: {e}")
        return None
    finally:
        # Fechar a sessão após a operação
        session.close()

def remover_tarefa(id: int):
    session = Session()
    try:
        tarefa = session.query(Tarefa).filter(Tarefa.id == id).first()
        if tarefa:
            session.delete(tarefa)
            session.commit()
            return True
        else:
            print(f"Tarefa com ID {id} não encontrada.")
            return False
    except Exception as e:
        session.rollback()
        print(f"Erro deletando tarefa: {e}")
        return False
    

# Atualizar
def atualizar_tarefa(tarefa_id: int, descricao: str, situacao: int):
    session = Session()
    try:
        tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        if tarefa:
            tarefa.descricao = descricao
            tarefa.situacao = situacao
            session.commit()
            session.refresh(tarefa)
            return tarefa
        else:
            print(f"Tarefa com ID {tarefa_id} não encontrada.")
            return None
    except Exception as e:
        session.rollback()
        print(f"Erro atualizando tarefa: {e}")
        return None