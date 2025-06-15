import streamlit as st
from typing import List, Dict, Any
from src.interface.book_interface import BookInterface
from src.interface.character_interface import CharacterInterface
from src.interface.environment_interface import EnvironmentInterface
from src.interface.chapter_interface import ChapterInterface
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
            
            logger.info("Criando instância do ChapterInterface")
            self.chapter_interface = ChapterInterface()
            logger.info("ChapterInterface criado com sucesso")
            
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
        elif st.session_state['current_view'] == 'manage_chapters':
            if 'selected_book' in st.session_state:
                logger.info(f"Exibindo gerenciamento de capítulos para o livro: {st.session_state['selected_book']['id']}")
                self.show_manage_chapters(st.session_state['selected_book'])
            else:
                logger.warning("Livro não selecionado")
                st.error("Livro não selecionado")
                st.session_state['current_view'] = 'list_books'
                st.experimental_rerun()

    def show_manage_chapters(self, book: Dict[str, Any]):
        """Exibe a interface de gerenciamento de capítulos."""
        logger.info(f"Exibindo gerenciamento de capítulos para o livro: {book['id']}")
        st.title(f"Gerenciar Capítulos - {book['titulo']}")
        
        # Informações do livro
        st.subheader("Informações do Livro")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Autor:** {book['autor']}")
            st.write(f"**Gênero:** {book['genero']}")
        with col2:
            st.write(f"**Volume:** {book['volume']}")
            st.write(f"**Idioma:** {book['idioma']}")
        
        st.divider()
        
        # Botão para criar novo capítulo
        if st.button("➕ Criar Novo Capítulo"):
            logger.info(f"Botão 'Criar Novo Capítulo' clicado para o livro: {book['id']}")
            st.session_state['current_view'] = 'create_chapter'
            st.session_state['selected_book'] = book
            st.experimental_rerun()
        
        # Lista de capítulos
        logger.info(f"Buscando capítulos para o livro: {book['id']}")
        try:
            chapters = self.chapter_interface.service.get_chapters_by_book_id(book['id'])
            logger.info(f"Encontrados {len(chapters) if chapters else 0} capítulos para o livro {book['id']}")
            
            if chapters:
                st.subheader("Capítulos")
                for chapter in chapters:
                    with st.container():
                        st.markdown("---")
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.markdown(f"### {chapter['titulo']}")
                            st.markdown(f"**Ordem:** {chapter['ordem']}")
                            if chapter['descricao_autor']:
                                st.markdown(f"**Descrição:** {chapter['descricao_autor']}")
                            st.markdown(f"**Texto:** {chapter['texto'][:200]}...")
                        with col2:
                            if st.button("✏️ Editar", key=f"edit_chapter_{chapter['id']}"):
                                logger.info(f"Botão 'Editar' clicado para o capítulo: {chapter['id']}")
                                st.session_state['current_view'] = 'edit_chapter'
                                st.session_state['selected_chapter'] = chapter
                                st.experimental_rerun()
                        with col3:
                            if st.button("🗑️ Excluir", key=f"delete_chapter_{chapter['id']}"):
                                logger.info(f"Botão 'Excluir' clicado para o capítulo: {chapter['id']}")
                                if self.chapter_interface.service.delete_chapter(chapter['id']):
                                    st.success("Capítulo excluído com sucesso!")
                                    st.experimental_rerun()
            else:
                logger.info(f"Nenhum capítulo encontrado para o livro: {book['id']}")
                st.info("Nenhum capítulo encontrado para este livro. Clique em 'Criar Novo Capítulo' para adicionar um.")
        except Exception as e:
            logger.error(f"Erro ao carregar capítulos do livro {book['id']}: {str(e)}", exc_info=True)
            st.error(f"Erro ao carregar capítulos: {str(e)}")
        
        # Botão para voltar
        if st.button("⬅️ Voltar para Lista de Livros"):
            logger.info("Botão 'Voltar para Lista de Livros' clicado")
            st.session_state['current_view'] = 'list_books'
            st.experimental_rerun() 