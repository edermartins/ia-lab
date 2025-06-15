import streamlit as st
from typing import List, Dict, Any
from src.interface.book_interface import BookInterface
from src.interface.character_interface import CharacterInterface
from src.interface.environment_interface import EnvironmentInterface
from src.utils.logger import logger
from src.utils.interface_utils import (
    print_header,
    print_success,
    print_error,
    print_warning,
    get_input,
    get_yes_no_input,
    clear_screen,
    print_table
)

class MainInterface:
    def __init__(self):
        """Inicializa a interface principal."""
        logger.info("Iniciando inicialização da MainInterface")
        try:
            # Inicializar interfaces
            logger.info("Criando instância do BookInterface")
            self.book_interface = BookInterface()
            logger.info("BookInterface criado com sucesso")
            
            logger.info("Criando instância do EnvironmentInterface")
            self.environment_interface = EnvironmentInterface()
            logger.info("EnvironmentInterface criado com sucesso")
            
            logger.info("MainInterface inicializada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar MainInterface: {str(e)}", exc_info=True)
            raise

    def show_interface(self):
        """Exibe a interface principal."""
        logger.info("Iniciando exibição da interface")
        
        # Inicializar o estado da sessão se necessário
        if 'current_view' not in st.session_state:
            logger.info("Inicializando estado da sessão")
            st.session_state['current_view'] = 'list_books'
        
        # Exibir a visualização atual
        logger.info(f"Visualização atual: {st.session_state['current_view']}")
        
        if st.session_state['current_view'] == 'list_books':
            logger.info("Exibindo lista de livros")
            self.book_interface.show_books_list()
        elif st.session_state['current_view'] == 'create_book':
            logger.info("Exibindo formulário de criação de livro")
            self.book_interface.show_create_book()
        elif st.session_state['current_view'] == 'edit_book':
            if 'selected_book' in st.session_state:
                logger.info(f"Exibindo formulário de edição do livro: {st.session_state['selected_book']['id']}")
                self.book_interface.show_edit_book(st.session_state['selected_book'])
            else:
                logger.warning("Livro não selecionado")
                st.error("Livro não selecionado")
                st.session_state['current_view'] = 'list_books'
                st.experimental_rerun()
        elif st.session_state['current_view'] == 'create_chapter':
            if 'selected_book' in st.session_state:
                logger.info(f"Exibindo formulário de criação de capítulo para o livro: {st.session_state['selected_book']['id']}")
                self.chapter_interface.show_create_chapter(st.session_state['selected_book']['id'])
            else:
                logger.warning("Livro não selecionado")
                st.error("Livro não selecionado")
                st.session_state['current_view'] = 'list_books'
                st.experimental_rerun()
        elif st.session_state['current_view'] == 'edit_chapter':
            if 'selected_chapter' in st.session_state:
                logger.info(f"Exibindo formulário de edição do capítulo: {st.session_state['selected_chapter']['id']}")
                self.chapter_interface.show_edit_chapter(st.session_state['selected_chapter'])
            else:
                logger.warning("Capítulo não selecionado")
                st.error("Capítulo não selecionado")
                st.session_state['current_view'] = 'edit_book'
                st.experimental_rerun() 