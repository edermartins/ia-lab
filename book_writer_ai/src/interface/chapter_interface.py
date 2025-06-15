import streamlit as st
from typing import List, Dict, Any
from src.services.chapter_service import ChapterService
from src.utils.logger import logger

class ChapterInterface:
    def __init__(self):
        """Inicializa a interface de capítulos."""
        logger.info("Iniciando inicialização da ChapterInterface")
        self.service = ChapterService()
        logger.info("ChapterInterface inicializada com sucesso")

    def show_create_chapter(self, book_id: str):
        """Exibe o formulário de criação de capítulo."""
        logger.info(f"Iniciando criação de capítulo para o livro: {book_id}")
        st.title("Criar Novo Capítulo")
        
        with st.form("create_chapter_form"):
            titulo = st.text_input("Título")
            ordem = st.number_input("Ordem", min_value=1, value=1)
            descricao_autor = st.text_area("Descrição do Autor")
            texto = st.text_area("Texto do Capítulo", height=300)
            
            submitted = st.form_submit_button("Criar")
            if submitted:
                logger.info(f"Formulário de criação de capítulo submetido para o livro: {book_id}")
                chapter_data = {
                    "livro_id": book_id,
                    "titulo": titulo,
                    "ordem": ordem,
                    "descricao_autor": descricao_autor,
                    "texto": texto
                }
                try:
                    new_chapter = self.service.create_chapter(chapter_data)
                    st.success("Capítulo criado com sucesso!")
                    st.session_state['current_view'] = 'edit_book'
                    st.experimental_rerun()
                except Exception as e:
                    logger.error(f"Erro ao criar capítulo: {str(e)}", exc_info=True)
                    st.error(f"Erro ao criar capítulo: {str(e)}")
        
        if st.button("Voltar"):
            logger.info("Botão 'Voltar' clicado")
            st.session_state['current_view'] = 'edit_book'
            st.experimental_rerun()

    def show_edit_chapter(self, chapter: Dict[str, Any]):
        """Exibe o formulário de edição de capítulo."""
        logger.info(f"Iniciando edição do capítulo: {chapter['id']} - {chapter['titulo']}")
        st.title(f"Editando: {chapter['titulo']}")
        
        with st.form("edit_chapter_form"):
            titulo = st.text_input("Título", value=chapter['titulo'])
            ordem = st.number_input("Ordem", min_value=1, value=chapter['ordem'])
            descricao_autor = st.text_area("Descrição do Autor", value=chapter['descricao_autor'])
            texto = st.text_area("Texto do Capítulo", value=chapter['texto'], height=300)
            
            submitted = st.form_submit_button("Salvar")
            if submitted:
                logger.info(f"Formulário de edição do capítulo {chapter['id']} submetido")
                chapter_data = {
                    "titulo": titulo,
                    "ordem": ordem,
                    "descricao_autor": descricao_autor,
                    "texto": texto
                }
                try:
                    updated_chapter = self.service.update_chapter(chapter['id'], chapter_data)
                    st.success("Capítulo atualizado com sucesso!")
                    st.session_state['current_view'] = 'edit_book'
                    st.experimental_rerun()
                except Exception as e:
                    logger.error(f"Erro ao atualizar capítulo: {str(e)}", exc_info=True)
                    st.error(f"Erro ao atualizar capítulo: {str(e)}")
        
        if st.button("Voltar"):
            logger.info("Botão 'Voltar' clicado")
            st.session_state['current_view'] = 'edit_book'
            st.experimental_rerun() 