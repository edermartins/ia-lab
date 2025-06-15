import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from src.utils.logger import logger

# Configuração do banco de dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'src', 'database.db')}"

logger.info(f"Diretório base: {BASE_DIR}")
logger.info(f"URL do banco de dados: {DATABASE_URL}")

# Criar o engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necessário para SQLite
)

# Criar a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar a base para os modelos
Base = declarative_base()

def init_db():
    """Inicializa o banco de dados criando todas as tabelas."""
    try:
        logger.info("Inicializando banco de dados...")
        # Importar os modelos aqui para garantir que todas as tabelas sejam criadas
        from src.models.book import Book
        
        # Verificar se o banco já existe
        db_exists = os.path.exists(os.path.join(BASE_DIR, 'src', 'database.db'))
        logger.info(f"Banco de dados {'existe' if db_exists else 'não existe'}")
        
        if db_exists:
            logger.info("Banco de dados já existe, não será recriado")
            return
        
        # Criar novas tabelas
        logger.debug("Criando novas tabelas...")
        Base.metadata.create_all(bind=engine)
        
        logger.info("Banco de dados inicializado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {str(e)}", exc_info=True)
        raise

@contextmanager
def get_db() -> Session:
    """
    Context manager para obter uma sessão do banco de dados.
    
    Yields:
        Session: Sessão do banco de dados
    """
    db = SessionLocal()
    try:
        logger.debug("Iniciando sessão do banco de dados")
        yield db
    except Exception as e:
        logger.error(f"Erro na sessão do banco de dados: {str(e)}", exc_info=True)
        db.rollback()
        raise
    finally:
        logger.debug("Fechando sessão do banco de dados")
        db.close() 