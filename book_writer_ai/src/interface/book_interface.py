import streamlit as st
from typing import List, Dict, Any
from src.services.book_service import BookService
from src.services.chapter_service import ChapterService
from src.utils.logger import logger

class BookInterface:
    def __init__(self):
        """Inicializa a interface de livros."""
        logger.info("Iniciando inicialização da BookInterface")
        try:
            self.service = BookService()
            self.chapter_service = ChapterService()
            logger.info("BookService e ChapterService inicializados com sucesso")
            logger.info("BookInterface inicializada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar BookInterface: {str(e)}", exc_info=True)
            raise

    def show_books_list(self, sidebar=False):
        """Exibe a lista de livros."""
        print(">>> Entrou na função show_books_list")
        logger.info("Exibindo lista de livros")
        st.title("Gerenciamento de Livros") if not sidebar else None
        
        # Lista de livros
        books = self.service.get_all_books()
        logger.info(f"Quantidade de livros encontrados: {len(books) if books else 0}")
        if books:
            for book in books:
                logger.info(f"Renderizando expander para o livro: {book['id']} - {book['titulo']}")
                with st.expander(f"{book['titulo']} - Volume {book['volume']}"):
                    st.write(f"**Autor:** {book['autor']}")
                    st.write(f"**Gênero:** {book['genero']}")
                    st.write(f"**Idioma:** {book['idioma']}")
                    st.write(f"**Estilo Narrativo:** {book['estilo_narrativo']}")
                    st.write(f"**Público Alvo:** {book['publico_alvo']}")
                    st.write(f"**Sinopse:** {book['sinopse']}")
                    logger.info(f"Criando colunas de botões para o livro: {book['id']}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        logger.info(f"Renderizando botão Editar para o livro: {book['id']}")
                        if st.button("Editar", key=f"edit_{book['id']}"):
                            logger.info(f"Botão 'Editar' clicado para o livro: {book['id']}")
                            st.session_state['current_view'] = 'edit_book'
                            st.session_state['selected_book'] = book
                            st.rerun()
                    with col2:
                        logger.info(f"Renderizando botão Capítulos para o livro: {book['id']}")
                        if st.button("Capítulos", key=f"manage_chapters_{book['id']}"):
                            logger.info(f"Botão 'Gerenciar Capítulos' clicado para o livro: {book['id']}")
                            st.session_state['current_view'] = 'manage_chapters'
                            st.session_state['selected_book'] = book
                            st.rerun()
                    with col3:
                        logger.info(f"Renderizando botão Excluir para o livro: {book['id']}")
                        if st.button("Excluir", key=f"delete_{book['id']}"):
                            logger.info(f"Botão 'Excluir' clicado para o livro: {book['id']}")
                            if self.service.delete_book(book['id']):
                                st.success("Livro excluído com sucesso!")
                                st.rerun()
        else:
            logger.info("Nenhum livro cadastrado.")
            st.info("Nenhum livro cadastrado.")

    def show_edit_book(self, book: Dict[str, Any]):
        """Exibe o formulário de edição de livro."""
        logger.info(f"Exibindo formulário de edição do livro: {book['id']}")
        st.title(f"Editando: {book['titulo']}")
        
        with st.form("edit_book_form"):
            titulo = st.text_input("Título", value=book['titulo'])
            volume = st.text_input("Volume", value=book['volume'])
            autor = st.text_input("Autor", value=book['autor'])
            genero = st.text_input("Gênero", value=book['genero'])
            idioma = st.text_input("Idioma", value=book['idioma'])
            sinopse = st.text_area("Sinopse", value=book['sinopse'])
            estilo_narrativo = st.text_input("Estilo Narrativo", value=book['estilo_narrativo'])
            publico_alvo = st.text_input("Público Alvo", value=book['publico_alvo'])
            
            submitted = st.form_submit_button("Salvar")
            if submitted:
                logger.info(f"Formulário de edição do livro {book['id']} submetido")
                book_data = {
                    "titulo": titulo,
                    "volume": volume,
                    "autor": autor,
                    "genero": genero,
                    "idioma": idioma,
                    "sinopse": sinopse,
                    "estilo_narrativo": estilo_narrativo,
                    "publico_alvo": publico_alvo
                }
                updated_book = self.service.update_book(book['id'], book_data)
                st.success("Livro atualizado com sucesso!")
                st.session_state['selected_book'] = updated_book
        
        # Botão para voltar
        if st.button("Voltar para Lista de Livros"):
            logger.info("Botão 'Voltar para Lista de Livros' clicado")
            st.session_state['current_view'] = 'list_books'
            st.rerun()

    def show_create_book(self):
        """Exibe o formulário de criação de livro."""
        st.title("Criar Novo Livro")
        
        with st.form("create_book_form"):
            titulo = st.text_input("Título")
            volume = st.text_input("Volume")
            autor = st.text_input("Autor")
            genero = st.text_input("Gênero")
            idioma = st.text_input("Idioma")
            sinopse = st.text_area("Sinopse")
            estilo_narrativo = st.text_input("Estilo Narrativo")
            publico_alvo = st.text_input("Público Alvo")
            
            submitted = st.form_submit_button("Criar")
            if submitted:
                book_data = {
                    "titulo": titulo,
                    "volume": volume,
                    "autor": autor,
                    "genero": genero,
                    "idioma": idioma,
                    "sinopse": sinopse,
                    "estilo_narrativo": estilo_narrativo,
                    "publico_alvo": publico_alvo
                }
                book = self.service.create_book(book_data)
                st.success("Livro criado com sucesso!")
                st.session_state['current_view'] = 'list_books'
                st.rerun()
        
        if st.button("Voltar para Lista de Livros"):
            st.session_state['current_view'] = 'list_books'
            st.rerun() 