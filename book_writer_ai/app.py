import streamlit as st
import google.generativeai as genai
import json
import hashlib
from datetime import datetime
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar a API do Google
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Configuração da página
st.set_page_config(page_title="Assistente de Escrita de Livros", page_icon="📚")

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

# Função para gerar hash único
def generate_id():
    return hashlib.md5(str(datetime.now()).encode()).hexdigest()

# Função para carregar livros
def load_books():
    if os.path.exists('books.json'):
        with open('books.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Função para salvar livros
def save_books(books):
    with open('books.json', 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

# Função para gerar sugestões
def generate_suggestions(description):
    prompt = SUGGESTION_TEMPLATE.format(description=description)
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return None

# Interface principal
st.title("📚 Assistente de Escrita de Livros")

# Sidebar para navegação
page = st.sidebar.selectbox("Navegação", ["Criar Livro", "Listar Livros", "Editar Livro", "Excluir Livro"])

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
            books = load_books()
            new_book = {
                "id": generate_id(),
                "titulo": titulo,
                "volume": volume,
                "autor": autor,
                "genero": genero,
                "idioma": idioma
            }
            books.append(new_book)
            save_books(books)
            st.success("Livro salvo com sucesso!")
            st.session_state.suggestions = None
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

elif page == "Listar Livros":
    st.header("Lista de Livros")
    books = load_books()
    
    if not books:
        st.info("Nenhum livro cadastrado.")
    else:
        for book in books:
            with st.expander(f"{book['titulo']} - Volume {book['volume']}"):
                st.write(f"**Autor:** {book['autor']}")
                st.write(f"**Gênero:** {book['genero']}")
                st.write(f"**Idioma:** {book['idioma']}")
                st.write(f"**ID:** {book['id']}")

elif page == "Editar Livro":
    st.header("Editar Livro")
    books = load_books()
    
    if not books:
        st.info("Nenhum livro cadastrado para editar.")
    else:
        book_to_edit = st.selectbox(
            "Selecione o livro para editar",
            books,
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
                    for i, book in enumerate(books):
                        if book['id'] == book_to_edit['id']:
                            books[i].update({
                                "titulo": titulo,
                                "volume": volume,
                                "autor": autor,
                                "genero": genero,
                                "idioma": idioma
                            })
                            break
                    save_books(books)
                    st.success("Livro atualizado com sucesso!")
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios.")

elif page == "Excluir Livro":
    st.header("Excluir Livro")
    books = load_books()
    
    if not books:
        st.info("Nenhum livro cadastrado para excluir.")
    else:
        book_to_delete = st.selectbox(
            "Selecione o livro para excluir",
            books,
            format_func=lambda x: f"{x['titulo']} - Volume {x['volume']}"
        )
        
        if book_to_delete and st.button("Excluir Livro"):
            books = [book for book in books if book['id'] != book_to_delete['id']]
            save_books(books)
            st.success("Livro excluído com sucesso!") 