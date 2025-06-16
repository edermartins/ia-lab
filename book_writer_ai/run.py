import os
import sys
import streamlit as st
from src.services.book_service import BookService
from src.services.character_service import CharacterService
from src.services.environment_service import EnvironmentService
from src.config.settings import APP_NAME, APP_ICON
from src.utils.logger import logger
from src.database import init_db
from src.interface.book_interface import BookInterface
from src.interface.character_interface import CharacterInterface
from src.interface.environment_interface import EnvironmentInterface
from src.interface.main_interface import MainInterface

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

def main():
    # Inicializar o banco de dados
    init_db()
    
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=APP_ICON,
        layout="wide"
    )
    
    # Inicializar o estado da sessão
    if 'current_view' not in st.session_state:
        st.session_state['current_view'] = 'list_books'
    if 'selected_book' not in st.session_state:
        st.session_state['selected_book'] = None
    if 'suggested_character' not in st.session_state:
        st.session_state['suggested_character'] = {}
    if 'suggested_environment' not in st.session_state:
        st.session_state['suggested_environment'] = {}
    if 'editing_character' not in st.session_state:
        st.session_state['editing_character'] = None
    if 'editing_environment' not in st.session_state:
        st.session_state['editing_environment'] = None
    
    st.title(f"{APP_ICON} {APP_NAME}")
    
    # Inicializar os serviços
    book_service = BookService()
    character_service = CharacterService()
    environment_service = EnvironmentService()
    book_interface = BookInterface()
    character_interface = CharacterInterface()
    environment_interface = EnvironmentInterface()
    main_interface = MainInterface()
    
    # Sidebar para lista de livros, personagens e ambientes
    with st.sidebar:
        st.header("Meus Livros")
        book_interface.show_books_list(sidebar=True)
        st.header("Meus Personagens")
        character_interface.show_characters_list()
        st.header("Meus Ambientes")
        environment_interface.show_environments_list()
    
    # Área principal
    if st.session_state.get('current_view') == 'edit_book' and st.session_state.get('selected_book'):
        book_interface.show_edit_book(st.session_state['selected_book'])
    elif st.session_state.get('current_view') == 'edit_chapter' and st.session_state.get('selected_chapter'):
        main_interface.chapter_interface.show_edit_chapter(st.session_state['selected_chapter'])
    elif st.session_state.get('current_view') == 'manage_chapters' and st.session_state.get('selected_book'):
        main_interface.show_manage_chapters(st.session_state['selected_book'])
    elif st.session_state.get('current_view') == 'create_chapter' and st.session_state.get('selected_book'):
        main_interface.chapter_interface.show_create_chapter(st.session_state['selected_book']['id'])
    elif st.session_state['editing_character'] is not None:
        character = st.session_state['editing_character']
        st.header("Editar Personagem")
        
        with st.form("editar_personagem_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome", value=character['nome'])
                idade = st.number_input("Idade", value=character['idade'], min_value=0, max_value=150)
                papel = st.text_input("Papel", value=character['papel'])
            
            caracteristicas_fisicas = st.text_area("Características Físicas", value=character['caracteristicas_fisicas'], height=100)
            personalidade = st.text_area("Personalidade", value=character['personalidade'], height=100)
            historico = st.text_area("Histórico", value=character['historico'], height=150)
            
            col1, col2 = st.columns([1, 4])
            with col1:
                submitted = st.form_submit_button("Salvar Alterações")
            with col2:
                if st.form_submit_button("Cancelar"):
                    st.session_state['editing_character'] = None
                    st.rerun()
            
            if submitted:
                try:
                    character_data = {
                        "nome": nome,
                        "idade": idade,
                        "papel": papel,
                        "caracteristicas_fisicas": caracteristicas_fisicas,
                        "personalidade": personalidade,
                        "historico": historico
                    }
                    character_service.update_character(character['id'], character_data)
                    st.success("Personagem atualizado com sucesso!")
                    st.session_state['editing_character'] = None
                    st.rerun()
                except Exception as e:
                    logger.error(f"Erro ao atualizar personagem: {str(e)}", exc_info=True)
                    st.error("Erro ao atualizar personagem. Tente novamente.")
    
    elif st.session_state['editing_environment'] is not None:
        environment = st.session_state['editing_environment']
        st.header("Editar Ambiente")
        
        with st.form("editar_ambiente_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome", value=environment['nome'])
                tipo = st.text_input("Tipo", value=environment['tipo'])
            
            descricao = st.text_area("Descrição", value=environment['descricao'], height=100)
            atmosfera = st.text_area("Atmosfera", value=environment['atmosfera'], height=100)
            elementos_importantes = st.text_area("Elementos Importantes", value=environment['elementos_importantes'], height=100)
            significado = st.text_area("Significado", value=environment['significado'], height=150)
            
            col1, col2 = st.columns([1, 4])
            with col1:
                submitted = st.form_submit_button("Salvar Alterações")
            with col2:
                if st.form_submit_button("Cancelar"):
                    st.session_state['editing_environment'] = None
                    st.rerun()
            
            if submitted:
                try:
                    environment_data = {
                        "nome": nome,
                        "tipo": tipo,
                        "descricao": descricao,
                        "atmosfera": atmosfera,
                        "elementos_importantes": elementos_importantes,
                        "significado": significado
                    }
                    environment_service.update_environment(environment['id'], environment_data)
                    st.success("Ambiente atualizado com sucesso!")
                    st.session_state['editing_environment'] = None
                    st.rerun()
                except Exception as e:
                    logger.error(f"Erro ao atualizar ambiente: {str(e)}", exc_info=True)
                    st.error("Erro ao atualizar ambiente. Tente novamente.")
    
    else:
        # Abas para Livros, Personagens e Ambientes
        tab1, tab2, tab3 = st.tabs(["📚 Livros", "👤 Personagens", "🌍 Ambientes"])
        
        with tab1:
            st.header("Sugestões de Livros")
            
            # Campo para descrição
            description = st.text_area(
                "Descreva o livro que você quer escrever:",
                value="",
                height=150,
                help="Forneça detalhes sobre o enredo, personagens, tema ou qualquer outro aspecto relevante do livro."
            )
            
            if st.button("Gerar Sugestões", key="generate_book"):
                if description:
                    with st.spinner("Gerando sugestões..."):
                        try:
                            suggestions = book_service.generate_suggestions(description)
                            if suggestions:
                                # Armazenar a primeira sugestão no session_state
                                st.session_state['selected_book'] = suggestions[0]
                                st.success("Sugestão gerada com sucesso! Os campos foram preenchidos automaticamente.")
                            else:
                                st.warning("Não foi possível gerar sugestões. Tente novamente.")
                        except Exception as e:
                            logger.error(f"Erro ao gerar sugestões: {str(e)}", exc_info=True)
                            st.error("Erro ao gerar sugestões. Tente novamente.")
                else:
                    st.warning("Por favor, forneça uma descrição do livro.")
            
            # Formulário para adicionar novo livro
            st.header("Adicionar Novo Livro")
            
            with st.form("novo_livro_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    titulo = st.text_input("Título", value=(st.session_state.get('selected_book') or {}).get('titulo', ''))
                    volume = st.text_input("Volume", value=(st.session_state.get('selected_book') or {}).get('volume', ''))
                    autor = st.text_input("Autor", value=(st.session_state.get('selected_book') or {}).get('autor', ''))
                
                with col2:
                    genero = st.text_input("Gênero", value=(st.session_state.get('selected_book') or {}).get('genero', ''))
                    idioma = st.text_input("Idioma", value=(st.session_state.get('selected_book') or {}).get('idioma', ''))
                    estilo_narrativo = st.text_input("Estilo Narrativo", value=(st.session_state.get('selected_book') or {}).get('estilo_narrativo', ''))
                    publico_alvo = st.text_input("Público Alvo", value=(st.session_state.get('selected_book') or {}).get('publico_alvo', ''))
                
                sinopse = st.text_area("Sinopse", value=(st.session_state.get('selected_book') or {}).get('sinopse', ''), height=150)
                
                submitted = st.form_submit_button("Adicionar Livro")
                
                if submitted:
                    try:
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
                        book_service.create_book(book_data)
                        st.success("Livro adicionado com sucesso!")
                        # Limpar a sugestão após adicionar o livro
                        st.session_state['selected_book'] = None
                        st.rerun()
                    except Exception as e:
                        logger.error(f"Erro ao adicionar livro: {str(e)}", exc_info=True)
                        st.error("Erro ao adicionar livro. Tente novamente.")
        
        with tab2:
            st.header("Sugestões de Personagens")
            
            # Campo para descrição
            description = st.text_area(
                "Descreva o personagem que você quer criar:",
                value="",
                height=150,
                help="Forneça detalhes sobre a aparência, personalidade, papel na história ou qualquer outro aspecto relevante do personagem."
            )
            
            if st.button("Gerar Sugestões", key="generate_character"):
                if description:
                    with st.spinner("Gerando sugestões..."):
                        try:
                            suggestions = character_service.generate_suggestions(description)
                            if suggestions:
                                # Armazenar a primeira sugestão no session_state
                                st.session_state['suggested_character'] = suggestions[0]
                                st.success("Sugestão gerada com sucesso! Os campos foram preenchidos automaticamente.")
                            else:
                                st.warning("Não foi possível gerar sugestões. Tente novamente.")
                        except Exception as e:
                            logger.error(f"Erro ao gerar sugestões: {str(e)}", exc_info=True)
                            st.error("Erro ao gerar sugestões. Tente novamente.")
                else:
                    st.warning("Por favor, forneça uma descrição do personagem.")
            
            # Formulário para adicionar novo personagem
            st.header("Adicionar Novo Personagem")
            
            with st.form("novo_personagem_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input("Nome", value=st.session_state.get('suggested_character', {}).get('nome', ''))
                    idade = st.number_input("Idade", value=st.session_state.get('suggested_character', {}).get('idade', 0), min_value=0, max_value=150)
                    papel = st.text_input("Papel", value=st.session_state.get('suggested_character', {}).get('papel', ''))
                
                caracteristicas_fisicas = st.text_area(
                    "Características Físicas",
                    value=st.session_state.get('suggested_character', {}).get('caracteristicas_fisicas', ''),
                    height=100
                )
                personalidade = st.text_area(
                    "Personalidade",
                    value=st.session_state.get('suggested_character', {}).get('personalidade', ''),
                    height=100
                )
                historico = st.text_area(
                    "Histórico",
                    value=st.session_state.get('suggested_character', {}).get('historico', ''),
                    height=150
                )
                
                submitted = st.form_submit_button("Adicionar Personagem")
                
                if submitted:
                    try:
                        character_data = {
                            "nome": nome,
                            "idade": idade,
                            "papel": papel,
                            "caracteristicas_fisicas": caracteristicas_fisicas,
                            "personalidade": personalidade,
                            "historico": historico
                        }
                        character_service.create_character(character_data)
                        st.success("Personagem adicionado com sucesso!")
                        # Limpar a sugestão após adicionar o personagem
                        st.session_state['suggested_character'] = {}
                        st.rerun()
                    except Exception as e:
                        logger.error(f"Erro ao adicionar personagem: {str(e)}", exc_info=True)
                        st.error("Erro ao adicionar personagem. Tente novamente.")
        
        with tab3:
            st.header("Sugestões de Ambientes")
            
            # Campo para descrição
            description = st.text_area(
                "Descreva o ambiente que você quer criar:",
                value="",
                height=150,
                help="Forneça detalhes sobre o tipo de ambiente, atmosfera, elementos importantes ou qualquer outro aspecto relevante."
            )
            
            if st.button("Gerar Sugestões", key="generate_environment"):
                if description:
                    with st.spinner("Gerando sugestões..."):
                        try:
                            suggestions = environment_service.generate_suggestions(description)
                            if suggestions:
                                # Armazenar a primeira sugestão no session_state
                                st.session_state['suggested_environment'] = suggestions[0]
                                st.success("Sugestão gerada com sucesso! Os campos foram preenchidos automaticamente.")
                            else:
                                st.warning("Não foi possível gerar sugestões. Tente novamente.")
                        except Exception as e:
                            logger.error(f"Erro ao gerar sugestões: {str(e)}", exc_info=True)
                            st.error("Erro ao gerar sugestões. Tente novamente.")
                else:
                    st.warning("Por favor, forneça uma descrição do ambiente.")
            
            # Formulário para adicionar novo ambiente
            st.header("Adicionar Novo Ambiente")
            
            with st.form("novo_ambiente_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input("Nome", value=st.session_state.get('suggested_environment', {}).get('nome', ''))
                    tipo = st.text_input("Tipo", value=st.session_state.get('suggested_environment', {}).get('tipo', ''))
                
                descricao = st.text_area(
                    "Descrição",
                    value=st.session_state.get('suggested_environment', {}).get('descricao', ''),
                    height=100
                )
                atmosfera = st.text_area(
                    "Atmosfera",
                    value=st.session_state.get('suggested_environment', {}).get('atmosfera', ''),
                    height=100
                )
                elementos_importantes = st.text_area(
                    "Elementos Importantes",
                    value=st.session_state.get('suggested_environment', {}).get('elementos_importantes', ''),
                    height=100
                )
                significado = st.text_area(
                    "Significado",
                    value=st.session_state.get('suggested_environment', {}).get('significado', ''),
                    height=150
                )
                
                submitted = st.form_submit_button("Adicionar Ambiente")
                
                if submitted:
                    try:
                        environment_data = {
                            "nome": nome,
                            "tipo": tipo,
                            "descricao": descricao,
                            "atmosfera": atmosfera,
                            "elementos_importantes": elementos_importantes,
                            "significado": significado
                        }
                        environment_service.create_environment(environment_data)
                        st.success("Ambiente adicionado com sucesso!")
                        # Limpar a sugestão após adicionar o ambiente
                        st.session_state['suggested_environment'] = {}
                        st.rerun()
                    except Exception as e:
                        logger.error(f"Erro ao adicionar ambiente: {str(e)}", exc_info=True)
                        st.error("Erro ao adicionar ambiente. Tente novamente.")

if __name__ == "__main__":
    main() 