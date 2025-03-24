# Este código configura e gerencia a conexão com um banco de dados MySQL usando SQLAlchemy.

from dotenv import load_dotenv  # Carrega variáveis de ambiente do arquivo .env
from sqlalchemy import create_engine  # Cria a conexão com o banco de dados
from sqlalchemy.orm import sessionmaker  # Gerencia sessões do banco de dados
import os
from model.tarefa_model import create_tables  # Função para criar tabelas no banco

load_dotenv()  # Carrega variáveis de ambiente, como usuário e senha do banco

# Classe de configuração para armazenar detalhes do banco de dados
class Config:
    DB_USER = os.getenv('DB_USER')  # O Usuário do banco
    DB_HOST = os.getenv('DB_HOST')  # O Host do banco
    DB_NAME = os.getenv('DB_NAME')  # Nome do banco
    DB_PASS = os.getenv('DB_PASSWORD')  # Senha do banco
    # Monta a URL de conexão com base nas variáveis de ambiente
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

# Cria o "engine", que faz a ponte entre o Python e o banco de dados
engine = create_engine(Config.DATABASE_URL)

# Configura o gerenciador de sessões
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    # Testa a conexão com o banco e tenta criar tabelas
    with engine.connect() as connection:
        print('Conexão bem sucedida')
        create_tables(engine)  # Chama a função para criar tabelas
except Exception as e:
    # Exibe mensagem de erro caso a conexão falhe
    print(f'Erro ao conectar: {e}')