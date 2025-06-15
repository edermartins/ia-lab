import logging
from src.database import init_db
from src.interface.main_interface import MainInterface
from src.utils.logger import logger
from src.models.book import Book
from src.models.character import Character
from src.models.environment import Environment

def main():
    """Função principal do programa."""
    try:
        logger.info("Iniciando aplicação...")
        
        # Inicializar banco de dados
        init_db()
        
        # Criar e exibir interface principal
        interface = MainInterface()
        
        logger.info("Aplicação finalizada com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao executar aplicação: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main() 