import streamlit as st
from src.interface.main_interface import MainInterface
from src.utils.logger import logger

def init_services():
    """Inicializa os serviços necessários."""
    logger.info("Inicializando serviços")
 
def init_interface(chapter_service):
    """Inicializa a interface principal."""
    logger.info("Inicializando interface principal")
    try:
        interface = MainInterface(chapter_service)
        logger.info("Interface principal inicializada com sucesso")
        return interface
    except Exception as e:
        logger.error(f"Erro ao inicializar interface principal: {str(e)}", exc_info=True)
        raise

def main():
    """Função principal da aplicação."""
    try:
        # Configurar a página
        st.set_page_config(
            page_title="Book Writer AI",
            page_icon="📚",
            layout="wide"
        )
        
    except Exception as e:
        logger.error(f"Erro na aplicação: {str(e)}", exc_info=True)
        st.error(f"Erro na aplicação: {str(e)}")

if __name__ == "__main__":
    main() 