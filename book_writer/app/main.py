import streamlit as st
from dotenv import load_dotenv
import os
from utils.llm_interface import LLMInterface
from components.character_editor import CharacterEditor
from components.environment_editor import EnvironmentEditor
from components.story_editor import StoryEditor

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração da página Streamlit
st.set_page_config(
    page_title="Book Writer - Assistente de Escrita com IA",
    page_icon="📚",
    layout="wide"
)

# Inicialização do LLM
llm_interface = LLMInterface()

# Título principal
st.title("📚 Book Writer - Assistente de Escrita com IA")

# Sidebar para navegação
st.sidebar.title("Navegação")
page = st.sidebar.radio(
    "Escolha uma seção:",
    ["Visão Geral", "Personagens", "Ambientes", "História", "Revisão"]
)

# Inicialização dos componentes
character_editor = CharacterEditor(llm_interface)
environment_editor = EnvironmentEditor(llm_interface)
story_editor = StoryEditor(llm_interface)

# Navegação entre páginas
if page == "Visão Geral":
    st.header("Bem-vindo ao Book Writer!")
    st.write("""
    Este aplicativo irá ajudá-lo a escrever seu livro usando IA. Você pode:
    - Criar e gerenciar personagens
    - Desenvolver ambientes e cenários
    - Escrever e estruturar sua história
    - Gerar diálogos entre personagens
    - Revisar e manter a coerência
    """)
    
    # Mostrar estatísticas do projeto
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Personagens", "0")
    with col2:
        st.metric("Ambientes", "0")
    with col3:
        st.metric("Capítulos", "0")

elif page == "Personagens":
    character_editor.render()

elif page == "Ambientes":
    environment_editor.render()

elif page == "História":
    story_editor.render()

elif page == "Revisão":
    st.header("Revisão e Coerência")
    st.write("""
    Aqui você pode revisar seu livro e garantir que todos os elementos
    estejam coerentes entre si.
    """)
    
    # Adicionar funcionalidades de revisão aqui

# Rodapé
st.sidebar.markdown("---")
st.sidebar.info(
    "Desenvolvido com ❤️ usando Streamlit, Google Gemini e LangChain"
) 