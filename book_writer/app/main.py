import streamlit as st
from dotenv import load_dotenv
import os
from utils.llm_interface import LLMInterface
from components.character_editor import CharacterEditor
from components.environment_editor import EnvironmentEditor
from components.story_editor import StoryEditor
from utils.environment_manager import EnvironmentManager
from database.models import Database

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração da página Streamlit
st.set_page_config(
    page_title="Book Writer",
    page_icon="📚",
    layout="wide"
)

# Inicialização do banco de dados
db = Database()

# Inicialização do LLM e managers
llm_interface = LLMInterface()
environment_manager = EnvironmentManager()

# Inicializa o estado da sessão para o livro atual
if "current_book_id" not in st.session_state:
    st.session_state.current_book_id = None

# Inicializa os componentes
character_editor = CharacterEditor(llm_interface)
environment_editor = EnvironmentEditor(llm_interface)
story_editor = StoryEditor(llm_interface)

# Sidebar para navegação
with st.sidebar:
    st.title("Navegação")
    
    # Seção de seleção/criação de livros
    st.subheader("Livros")
    
    # Lista de livros existentes
    stories = db.get_all_stories()
    if stories:
        for story in stories:
            if st.button(f"📚 {story['title']}", key=f"story_{story['id']}"):
                st.session_state.current_book_id = story['id']
                st.rerun()
    
    # Botão para criar novo livro
    if st.button("Novo Livro"):
        st.session_state.current_book_id = None
        st.session_state.page = "História"
        st.rerun()
    
    st.divider()
    
    # Menu de navegação
    if "page" not in st.session_state:
        st.session_state.page = "Visão Geral"
    
    page = st.radio(
        "Selecione uma seção:",
        ["Visão Geral", "Personagens", "Ambientes", "História"],
        key="page"
    )

# Área principal
if page == "Visão Geral":
    st.title("Visão Geral")
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        characters = db.get_book_characters(st.session_state.current_book_id) if st.session_state.current_book_id else {}
        st.metric("Personagens", len(characters))
        
        # Lista os 3 personagens mais recentes
        if characters:
            st.subheader("Personagens Recentes")
            for char_id, char in list(characters.items())[-3:]:
                st.write(f"👤 {char['name']}")
    
    with col2:
        environments = db.get_book_environments(st.session_state.current_book_id) if st.session_state.current_book_id else {}
        st.metric("Ambientes", len(environments))
        
        # Lista os 3 ambientes mais recentes
        if environments:
            st.subheader("Ambientes Recentes")
            for env_id, env in list(environments.items())[-3:]:
                st.write(f"🏠 {env['name']}")
    
    with col3:
        story = db.get_story(st.session_state.current_book_id) if st.session_state.current_book_id else None
        chapters = db.get_book_chapters(st.session_state.current_book_id) if st.session_state.current_book_id else {}
        st.metric("Capítulos", len(chapters))
        
        # Lista os 3 capítulos mais recentes
        if chapters:
            st.subheader("Capítulos Recentes")
            for chapter_id, chapter in list(chapters.items())[-3:]:
                st.write(f"📖 {chapter['title']}")

elif page == "Personagens":
    character_editor.render(st.session_state.current_book_id)

elif page == "Ambientes":
    environment_editor.render(st.session_state.current_book_id)

elif page == "História":
    story_editor.render(st.session_state.current_book_id)

# Rodapé
st.sidebar.markdown("---")
st.sidebar.info(
    "Desenvolvido com ❤️ usando Streamlit, Google Gemini e LangChain"
) 