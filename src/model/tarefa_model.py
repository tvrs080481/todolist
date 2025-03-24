# Define o modelo Tarefa e a criação de tabelas no banco de dados.

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer, Boolean

# Criação de uma base declarativa para os modelos
Base = declarative_base()

# Modelo Tarefa que representa a tabela 'tb_tarefa_taskforce' no banco de dados
class Tarefa(Base):
    __tablename__ = 'tb_tarefa_taskforce'

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID único e autoincrementado
    descricao = Column(Text, nullable=True)  # Descrição da tarefa, pode ser nula
    situacao = Column(Boolean, default=False)  # Situação (concluída ou não), padrão é False

    # Construtor para inicializar a tarefa com descrição e situação
    def __init__(self, descricao, situacao):
        self.descricao = descricao
        self.situacao = situacao

# Função para criar as tabelas no banco de dados a partir do modelo
def create_tables(engine):
    Base.metadata.create_all(engine)  # Gera as tabelas no banco com base nos modelos declarados