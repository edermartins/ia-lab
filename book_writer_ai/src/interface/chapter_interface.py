import streamlit as st
from typing import List, Dict, Any
from src.services.chapter_service import ChapterService
from src.utils.logger import logger
from src.services.character_service import CharacterService
from src.services.environment_service import EnvironmentService
from src.agents.chapter_suggestion_agent import ChapterSuggestionAgent

class ChapterInterface:
    def __init__(self):
        """Inicializa a interface de capítulos."""
        logger.info("Iniciando inicialização da ChapterInterface")
        self.service = ChapterService()
        logger.info("ChapterInterface inicializada com sucesso")

    def show_create_chapter(self, book_id: str):
        """Exibe o formulário de criação de capítulo com IA, seleção de personagens e ambientes."""
        logger.info(f"Iniciando criação de capítulo para o livro: {book_id}")
        st.title("Criar Novo Capítulo")

        # Serviços auxiliares
        character_service = CharacterService()
        environment_service = EnvironmentService()
        personagens = character_service.get_all_characters()
        ambientes = environment_service.get_all_environments()

        # Estado temporário para sugestão
        if 'chapter_suggestion' not in st.session_state:
            st.session_state['chapter_suggestion'] = {}

        # Campo de sugestão de IA
        sugestao_ia = st.text_area("Sugestão para IA (opcional)", value=st.session_state['chapter_suggestion'].get('sugestao_ia', ''))

        # Seleção de personagens
        personagens_opcoes = {p['nome']: p['id'] for p in personagens}
        personagens_selecionados = st.multiselect(
            "Personagens presentes no capítulo",
            options=list(personagens_opcoes.keys()),
            default=st.session_state['chapter_suggestion'].get('personagens', [])
        )

        # Lista de ambientes (múltipla escolha, pode ser nenhuma)
        ambientes_opcoes = {a['nome']: a['id'] for a in ambientes}
        ambientes_default = st.session_state['chapter_suggestion'].get('ambientes', [])
        if not isinstance(ambientes_default, list):
            ambientes_default = []
        ambientes_selecionados = st.multiselect(
            "Ambientes presentes no capítulo",
            options=list(ambientes_opcoes.keys()),
            default=ambientes_default
        )

        # Botão para gerar sugestão via IA
        if st.button("Gerar Sugestão com IA"):
            agent = ChapterSuggestionAgent()
            # Buscar dados completos dos personagens e ambientes selecionados
            personagens_escolhidos = [p for p in personagens if p['nome'] in personagens_selecionados]
            ambientes_escolhidos = [a for a in ambientes if a['nome'] in ambientes_selecionados]
            resposta = agent.generate_suggestion(sugestao_ia, personagens_escolhidos, ambientes_escolhidos)
            st.session_state['chapter_suggestion'] = {
                'sugestao_ia': sugestao_ia,
                'personagens': personagens_selecionados,
                'ambientes': ambientes_selecionados,
                'titulo': resposta.get('titulo', ''),
                'ordem': resposta.get('ordem', 1),
                'descricao_autor': sugestao_ia,
                'texto': resposta.get('texto', '')
            }
            st.rerun()

        with st.form("create_chapter_form"):
            titulo_form = st.text_input("Título", value=st.session_state['chapter_suggestion'].get('titulo', ''))
            ordem_form = st.number_input("Ordem", min_value=1, value=st.session_state['chapter_suggestion'].get('ordem', 1))
            descricao_autor_form = st.text_area("Descrição do Autor", value=st.session_state['chapter_suggestion'].get('descricao_autor', ''))
            texto_form = st.text_area("Texto do Capítulo", value=st.session_state['chapter_suggestion'].get('texto', ''), height=300)
            personagens_ids = [personagens_opcoes[n] for n in st.session_state['chapter_suggestion'].get('personagens', [])]
            ambientes_ids = [ambientes_opcoes[n] for n in st.session_state['chapter_suggestion'].get('ambientes', [])]

            submitted = st.form_submit_button("Criar")
            if submitted:
                logger.info(f"Formulário de criação de capítulo submetido para o livro: {book_id}")
                chapter_data = {
                    "book_id": book_id,
                    "titulo": titulo_form,
                    "ordem": ordem_form,
                    "descricao_autor": descricao_autor_form,
                    "texto": texto_form,
                    "personagens": personagens_ids,
                    "ambientes": ambientes_ids
                }
                try:
                    new_chapter = self.service.create_chapter(chapter_data)
                    st.success("Capítulo criado com sucesso!")
                    st.session_state['chapter_suggestion'] = {}
                    st.session_state['current_view'] = 'manage_chapters'
                    st.rerun()
                except Exception as e:
                    logger.error(f"Erro ao criar capítulo: {str(e)}", exc_info=True)
                    st.error(f"Erro ao criar capítulo: {str(e)}")

        if st.button("Voltar"):
            logger.info("Botão 'Voltar' clicado")
            st.session_state['chapter_suggestion'] = {}
            st.session_state['current_view'] = 'manage_chapters'
            st.rerun()

    def show_edit_chapter(self, chapter: Dict[str, Any]):
        """Exibe o formulário de edição de capítulo com IA, seleção de personagens e ambientes."""
        logger.info(f"Iniciando edição do capítulo: {chapter['id']} - {chapter['titulo']}")
        st.title(f"Editando: {chapter['titulo']}")

        # Serviços auxiliares
        character_service = CharacterService()
        environment_service = EnvironmentService()
        personagens = character_service.get_all_characters()
        ambientes = environment_service.get_all_environments()

        # Estado temporário para sugestão
        if 'chapter_edit_suggestion' not in st.session_state:
            st.session_state['chapter_edit_suggestion'] = {}

        # Campo de sugestão de IA
        sugestao_ia = st.text_area("Sugestão para IA (opcional)", value=st.session_state['chapter_edit_suggestion'].get('sugestao_ia', ''))

        # Seleção de personagens
        personagens_opcoes = {p['nome']: p['id'] for p in personagens}
        personagens_selecionados = st.multiselect(
            "Personagens presentes no capítulo",
            options=list(personagens_opcoes.keys()),
            default=st.session_state['chapter_edit_suggestion'].get('personagens', [p['nome'] for p in personagens if p['id'] in chapter.get('personagens', [])])
        )

        # Seleção de ambientes
        ambientes_opcoes = {a['nome']: a['id'] for a in ambientes}
        ambientes_selecionados = st.multiselect(
            "Ambientes presentes no capítulo",
            options=list(ambientes_opcoes.keys()),
            default=st.session_state['chapter_edit_suggestion'].get('ambientes', [a['nome'] for a in ambientes if a['id'] in chapter.get('ambientes', [])])
        )

        # Botão para gerar sugestão via IA
        if st.button("Gerar Sugestão com IA", key="edit_gerar_sugestao_ia"):
            agent = ChapterSuggestionAgent()
            # Buscar dados completos dos personagens e ambientes selecionados
            personagens_escolhidos = [p for p in personagens if p['nome'] in personagens_selecionados]
            ambientes_escolhidos = [a for a in ambientes if a['nome'] in ambientes_selecionados]
            resposta = agent.generate_suggestion(sugestao_ia, personagens_escolhidos, ambientes_escolhidos)
            st.session_state['chapter_edit_suggestion'] = {
                'sugestao_ia': sugestao_ia,
                'personagens': personagens_selecionados,
                'ambientes': ambientes_selecionados,
                'titulo': resposta.get('titulo', ''),
                'ordem': resposta.get('ordem', 1),
                'texto': resposta.get('texto', '')
            }
            st.rerun()

        # Campos do capítulo
        with st.form("edit_chapter_form"):
            titulo_form = st.text_input("Título", value=st.session_state['chapter_edit_suggestion'].get('titulo', chapter['titulo']))
            ordem_form = st.number_input("Ordem", min_value=1, value=st.session_state['chapter_edit_suggestion'].get('ordem', chapter['ordem']))
            texto_form = st.text_area("Texto do Capítulo", value=st.session_state['chapter_edit_suggestion'].get('texto', chapter['texto']), height=300)
            personagens_ids = [personagens_opcoes[n] for n in st.session_state['chapter_edit_suggestion'].get('personagens', [p['nome'] for p in personagens if p['id'] in chapter.get('personagens', [])])]
            ambientes_ids = [ambientes_opcoes[n] for n in st.session_state['chapter_edit_suggestion'].get('ambientes', [a['nome'] for a in ambientes if a['id'] in chapter.get('ambientes', [])])]

            submitted = st.form_submit_button("Salvar")
            if submitted:
                logger.info(f"Formulário de edição do capítulo {chapter['id']} submetido")
                chapter_data = {
                    "titulo": titulo_form,
                    "ordem": ordem_form,
                    "texto": texto_form,
                    "personagens": personagens_ids,
                    "ambientes": ambientes_ids
                }
                try:
                    updated_chapter = self.service.update_chapter(chapter['id'], chapter_data)
                    st.success("Capítulo atualizado com sucesso!")
                    st.session_state['chapter_edit_suggestion'] = {}
                    st.session_state['current_view'] = 'manage_chapters'
                    st.rerun()
                except Exception as e:
                    logger.error(f"Erro ao atualizar capítulo: {str(e)}", exc_info=True)
                    st.error(f"Erro ao atualizar capítulo: {str(e)}")

        if st.button("Voltar"):
            logger.info("Botão 'Voltar' clicado")
            st.session_state['chapter_edit_suggestion'] = {}
            st.session_state['current_view'] = 'manage_chapters'
            st.rerun() 