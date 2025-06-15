import streamlit as st
from typing import List, Dict, Any
from src.services.book_service import BookService
from src.utils.logger import logger

class BookInterface:
    def __init__(self):
        """Inicializa a interface de livros."""
        logger.info("Iniciando inicialização da BookInterface")
        try:
            self.service = BookService()
            logger.info("BookService inicializado com sucesso")

            
            logger.info("BookInterface inicializada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar BookInterface: {str(e)}", exc_info=True)
            raise

    def show_books_list(self):
        """Exibe a lista de livros."""
        logger.info("Exibindo lista de livros")
        st.title("Gerenciamento de Livros")
        
        # Criar novo livro
        if st.button("Criar Novo Livro"):
            logger.info("Botão 'Criar Novo Livro' clicado")
            st.session_state['current_view'] = 'create_book'
            st.experimental_rerun()
        
        # Lista de livros
        books = self.service.get_all_books()
        if books:
            logger.info(f"Encontrados {len(books)} livros")
            for book in books:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(book['titulo'])
                        st.write(f"Autor: {book['autor']}")
                        st.write(f"Gênero: {book['genero']}")
                    with col2:
                        if st.button("Editar", key=f"edit_{book['id']}"):
                            logger.info(f"Botão 'Editar' clicado para o livro: {book['id']}")
                            st.session_state['current_view'] = 'edit_book'
                            st.session_state['selected_book'] = book
                            st.experimental_rerun()
        else:
            logger.warning("Nenhum livro encontrado")
            st.warning("Nenhum livro encontrado.")

    def show_edit_book(self, book: Dict[str, Any]):
        """Exibe o formulário de edição de livro."""
        logger.info(f"Iniciando edição do livro: {book['id']} - {book['titulo']}")
        st.title(f"Editando: {book['titulo']}")
        
        # Formulário de edição
        with st.form("edit_book_form"):
            titulo = st.text_input("Título", value=book['titulo'])
            autor = st.text_input("Autor", value=book['autor'])
            genero = st.text_input("Gênero", value=book['genero'])
            sinopse = st.text_area("Sinopse", value=book['sinopse'])
            
            submitted = st.form_submit_button("Salvar")
            if submitted:
                logger.info(f"Formulário de edição do livro {book['id']} submetido")
                book_data = {
                    "titulo": titulo,
                    "autor": autor,
                    "genero": genero,
                    "sinopse": sinopse
                }
                updated_book = self.service.update_book(book['id'], book_data)
                st.success("Livro atualizado com sucesso!")
                st.session_state['selected_book'] = updated_book
        
        # Botão para voltar
        if st.button("Voltar para Lista de Livros"):
            logger.info("Botão 'Voltar para Lista de Livros' clicado")
            st.session_state['current_view'] = 'list_books'
            st.experimental_rerun()

    def show_create_book(self):
        """Exibe o formulário de criação de livro."""
        st.title("Criar Novo Livro")
        
        with st.form("create_book_form"):
            titulo = st.text_input("Título")
            autor = st.text_input("Autor")
            genero = st.text_input("Gênero")
            sinopse = st.text_area("Sinopse")
            
            submitted = st.form_submit_button("Criar")
            if submitted:
                book_data = {
                    "titulo": titulo,
                    "autor": autor,
                    "genero": genero,
                    "sinopse": sinopse
                }
                book = self.service.create_book(book_data)
                st.success("Livro criado com sucesso!")
                st.session_state['current_view'] = 'list_books'
                st.experimental_rerun()
        
        if st.button("Voltar para Lista de Livros"):
            st.session_state['current_view'] = 'list_books'
            st.experimental_rerun() 