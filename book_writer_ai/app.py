import streamlit as st
import google.generativeai as genai
import json
import hashlib
from datetime import datetime
import os
from dotenv import load_dotenv
from src.services.book_service import BookService
from src.services.chapter_service import ChapterService
from src.services.character_service import CharacterService
from src.services.environment_service import EnvironmentService
from src.database import init_db
import uuid

# Carregar variáveis de ambiente
load_dotenv()

# Configurar a API do Google
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Configuração da página
st.set_page_config(page_title="Assistente de Escrita de Livros", page_icon="📚")

# Inicializar o banco de dados
init_db()

# Inicializar o modelo Gemini
model = genai.GenerativeModel('gemini-2.0-flash')

# Template para geração de sugestões
SUGGESTION_TEMPLATE = """
Com base na seguinte descrição, sugira os detalhes para um livro:
{description}

Por favor, forneça uma resposta no seguinte formato JSON:
{{
    "titulo": "Título sugerido",
    "volume": "Volume sugerido",
    "autor": "Nome do autor sugerido",
    "genero": "Gênero sugerido",
    "idioma": "Idioma sugerido"
}}
"""

# Template para geração de sugestões de capítulo
CHAPTER_SUGGESTION_TEMPLATE = """
Com base na seguinte descrição, sugira o conteúdo para um capítulo:
Descrição do autor: {author_description}
Personagens envolvidos: {characters}
Ambientes: {environments}

Por favor, forneça uma resposta no seguinte formato JSON:
{{
    "titulo": "Título do capítulo",
    "texto": "Conteúdo do capítulo"
}}
"""

# Função para gerar hash único
def generate_id():
    return hashlib.md5(str(datetime.now()).encode()).hexdigest()

# Função para gerar sugestões
def generate_suggestions(description):
    prompt = SUGGESTION_TEMPLATE.format(description=description)
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return None

# Inicializar serviços
book_service = BookService()
chapter_service = ChapterService()
character_service = CharacterService()
environment_service = EnvironmentService()

# Interface principal
st.title("📚 Assistente de Escrita de Livros")

# Sidebar para navegação
page = st.sidebar.selectbox("Navegação", [
    "Criar Livro", 
    "Listar Livros", 
    "Editar Livro", 
    "Excluir Livro",
    "Gerenciar Capítulos",
    "Gerenciar Personagens",
    "Gerenciar Ambientes"
])

if page == "Criar Livro":
    st.header("Criar Novo Livro")
    
    # Campo de descrição
    description = st.text_area("Descrição do Livro (opcional)", height=150)
    
    if st.button("Gerar Sugestões"):
        if description:
            with st.spinner("Gerando sugestões..."):
                suggestions = generate_suggestions(description)
                if suggestions:
                    st.session_state.suggestions = suggestions
                else:
                    st.error("Não foi possível gerar sugestões. Tente novamente.")
    
    # Campos do formulário
    if 'suggestions' in st.session_state:
        suggestions = st.session_state.suggestions
    else:
        suggestions = {
            "titulo": "",
            "volume": "",
            "autor": "",
            "genero": "",
            "idioma": ""
        }
    
    titulo = st.text_input("Título", value=suggestions.get("titulo", ""))
    volume = st.text_input("Volume", value=suggestions.get("volume", ""))
    autor = st.text_input("Autor", value=suggestions.get("autor", ""))
    genero = st.text_input("Gênero", value=suggestions.get("genero", ""))
    idioma = st.text_input("Idioma", value=suggestions.get("idioma", ""))
    
    if st.button("Salvar Livro"):
        if titulo and volume and autor and genero and idioma:
            new_book = {
                "titulo": titulo,
                "volume": volume,
                "autor": autor,
                "genero": genero,
                "idioma": idioma
            }
            book_service.create_book(new_book)
            st.success("Livro salvo com sucesso!")
            st.session_state.suggestions = None
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

elif page == "Listar Livros":
    st.header("Lista de Livros")
    books = book_service.get_all_books()
    
    if not books:
        st.info("Nenhum livro cadastrado.")
    else:
        for book in books:
            with st.expander(f"{book['titulo']} - Volume {book['volume']}"):
                st.write(f"**Autor:** {book['autor']}")
                st.write(f"**Gênero:** {book['genero']}")
                st.write(f"**Idioma:** {book['idioma']}")

elif page == "Editar Livro":
    st.header("Editar Livro")
    
    if not book_service.get_all_books():
        st.info("Nenhum livro cadastrado para editar.")
    else:
        book_to_edit = st.selectbox(
            "Selecione o livro para editar",
            book_service.get_all_books(),
            format_func=lambda x: f"{x['titulo']} - Volume {x['volume']}"
        )
        
        if book_to_edit:
            titulo = st.text_input("Título", value=book_to_edit['titulo'])
            volume = st.text_input("Volume", value=book_to_edit['volume'])
            autor = st.text_input("Autor", value=book_to_edit['autor'])
            genero = st.text_input("Gênero", value=book_to_edit['genero'])
            idioma = st.text_input("Idioma", value=book_to_edit['idioma'])
            
            if st.button("Atualizar Livro"):
                if titulo and volume and autor and genero and idioma:
                    book_to_edit.update({
                        "titulo": titulo,
                        "volume": volume,
                        "autor": autor,
                        "genero": genero,
                        "idioma": idioma
                    })
                    book_service.update_book(book_to_edit)
                    st.success("Livro atualizado com sucesso!")
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios.")

elif page == "Excluir Livro":
    st.header("Excluir Livro")
    books = book_service.get_all_books()
    
    if not books:
        st.info("Nenhum livro cadastrado para excluir.")
    else:
        book_to_delete = st.selectbox(
            "Selecione o livro para excluir",
            books,
            format_func=lambda x: f"{x['titulo']} - Volume {x['volume']}"
        )
        
        if book_to_delete and st.button("Excluir Livro"):
            book_service.delete_book(book_to_delete['id'])
            st.success("Livro excluído com sucesso!")

elif page == "Gerenciar Personagens":
    st.header("Gerenciar Personagens")
    
    # Submenu para ações com personagens
    character_action = st.radio(
        "Ação",
        ["Criar Personagem", "Listar Personagens", "Editar Personagem", "Excluir Personagem"]
    )
    
    if character_action == "Criar Personagem":
        st.subheader("Criar Novo Personagem")
        
        # Campos do formulário
        character_name = st.text_input("Nome do Personagem")
        character_description = st.text_area("Descrição do Personagem", height=150)
        character_background = st.text_area("Histórico do Personagem", height=200)
        character_traits = st.text_area("Características do Personagem", height=150)
        
        if st.button("Salvar Personagem"):
            if character_name:
                new_character = {
                    "nome": character_name,
                    "descricao": character_description,
                    "historico": character_background,
                    "caracteristicas": character_traits
                }
                character_service.create_character(new_character)
                st.success("Personagem salvo com sucesso!")
            else:
                st.error("Por favor, preencha o nome do personagem.")
    
    elif character_action == "Listar Personagens":
        st.subheader("Lista de Personagens")
        if not character_service.get_all_characters():
            st.info("Nenhum personagem cadastrado.")
        else:
            for character in character_service.get_all_characters():
                with st.expander(f"{character['nome']}"):
                    st.write(f"**Descrição:** {character['descricao']}")
                    st.write(f"**Histórico:** {character['historico']}")
                    st.write(f"**Características:** {character['caracteristicas']}")
    
    elif character_action == "Editar Personagem":
        st.subheader("Editar Personagem")
        if not character_service.get_all_characters():
            st.info("Nenhum personagem cadastrado para editar.")
        else:
            character_to_edit = st.selectbox(
                "Selecione o personagem para editar",
                character_service.get_all_characters(),
                format_func=lambda x: x['nome']
            )
            
            if character_to_edit:
                character_name = st.text_input("Nome do Personagem", value=character_to_edit['nome'])
                character_description = st.text_area("Descrição do Personagem", value=character_to_edit['descricao'], height=150)
                character_background = st.text_area("Histórico do Personagem", value=character_to_edit['historico'], height=200)
                character_traits = st.text_area("Características do Personagem", value=character_to_edit['caracteristicas'], height=150)
                
                if st.button("Atualizar Personagem"):
                    if character_name:
                        character_to_edit.update({
                            "nome": character_name,
                            "descricao": character_description,
                            "historico": character_background,
                            "caracteristicas": character_traits
                        })
                        character_service.update_character(character_to_edit)
                        st.success("Personagem atualizado com sucesso!")
                    else:
                        st.error("Por favor, preencha o nome do personagem.")
    
    elif character_action == "Excluir Personagem":
        st.subheader("Excluir Personagem")
        if not character_service.get_all_characters():
            st.info("Nenhum personagem cadastrado para excluir.")
        else:
            character_to_delete = st.selectbox(
                "Selecione o personagem para excluir",
                character_service.get_all_characters(),
                format_func=lambda x: x['nome']
            )
            
            if character_to_delete and st.button("Excluir Personagem"):
                character_service.delete_character(character_to_delete['id'])
                st.success("Personagem excluído com sucesso!")

elif page == "Gerenciar Ambientes":
    st.header("Gerenciar Ambientes")
    
    # Submenu para ações com ambientes
    environment_action = st.radio(
        "Ação",
        ["Criar Ambiente", "Listar Ambientes", "Editar Ambiente", "Excluir Ambiente"]
    )
    
    if environment_action == "Criar Ambiente":
        st.subheader("Criar Novo Ambiente")
        
        # Campos do formulário
        environment_name = st.text_input("Nome do Ambiente")
        environment_description = st.text_area("Descrição do Ambiente", height=150)
        environment_details = st.text_area("Detalhes do Ambiente", height=200)
        environment_atmosphere = st.text_area("Atmosfera do Ambiente", height=150)
        
        if st.button("Salvar Ambiente"):
            if environment_name:
                new_environment = {
                    "nome": environment_name,
                    "descricao": environment_description,
                    "detalhes": environment_details,
                    "atmosfera": environment_atmosphere
                }
                environment_service.create_environment(new_environment)
                st.success("Ambiente salvo com sucesso!")
            else:
                st.error("Por favor, preencha o nome do ambiente.")
    
    elif environment_action == "Listar Ambientes":
        st.subheader("Lista de Ambientes")
        if not environment_service.get_all_environments():
            st.info("Nenhum ambiente cadastrado.")
        else:
            for environment in environment_service.get_all_environments():
                with st.expander(f"{environment['nome']}"):
                    st.write(f"**Descrição:** {environment['descricao']}")
                    st.write(f"**Detalhes:** {environment['detalhes']}")
                    st.write(f"**Atmosfera:** {environment['atmosfera']}")
    
    elif environment_action == "Editar Ambiente":
        st.subheader("Editar Ambiente")
        if not environment_service.get_all_environments():
            st.info("Nenhum ambiente cadastrado para editar.")
        else:
            environment_to_edit = st.selectbox(
                "Selecione o ambiente para editar",
                environment_service.get_all_environments(),
                format_func=lambda x: x['nome']
            )
            
            if environment_to_edit:
                environment_name = st.text_input("Nome do Ambiente", value=environment_to_edit['nome'])
                environment_description = st.text_area("Descrição do Ambiente", value=environment_to_edit['descricao'], height=150)
                environment_details = st.text_area("Detalhes do Ambiente", value=environment_to_edit['detalhes'], height=200)
                environment_atmosphere = st.text_area("Atmosfera do Ambiente", value=environment_to_edit['atmosfera'], height=150)
                
                if st.button("Atualizar Ambiente"):
                    if environment_name:
                        environment_to_edit.update({
                            "nome": environment_name,
                            "descricao": environment_description,
                            "detalhes": environment_details,
                            "atmosfera": environment_atmosphere
                        })
                        environment_service.update_environment(environment_to_edit)
                        st.success("Ambiente atualizado com sucesso!")
                    else:
                        st.error("Por favor, preencha o nome do ambiente.")
    
    elif environment_action == "Excluir Ambiente":
        st.subheader("Excluir Ambiente")
        if not environment_service.get_all_environments():
            st.info("Nenhum ambiente cadastrado para excluir.")
        else:
            environment_to_delete = st.selectbox(
                "Selecione o ambiente para excluir",
                environment_service.get_all_environments(),
                format_func=lambda x: x['nome']
            )
            
            if environment_to_delete and st.button("Excluir Ambiente"):
                environment_service.delete_environment(environment_to_delete['id'])
                st.success("Ambiente excluído com sucesso!")

# Adicionar o botão "Gerenciar Capítulos" no menu lateral
st.header("Capítulos do Livro Selecionado")
if 'editing_book' in st.session_state and st.session_state['editing_book'] is not None:
    if st.button("Gerenciar Capítulos"):
        st.session_state['manage_chapters'] = True
        st.rerun()
else:
    st.info("Selecione um livro para gerenciar capítulos.")

if st.session_state.get('manage_chapters', False):
    from src.ui.pages import manage_chapters
    manage_chapters.render(st.session_state['editing_book'])

st.header("Gerenciar Livros") 