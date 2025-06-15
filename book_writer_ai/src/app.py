import streamlit as st
from config.settings import APP_NAME, APP_ICON
from ui.pages import create_book, list_books, edit_book, delete_book
from services.database import init_db

def main():
    # Configuração da página
    st.set_page_config(page_title=APP_NAME, page_icon=APP_ICON)
    
    # Inicializar banco de dados
    init_db()
    
    # Título principal
    st.title(f"{APP_ICON} {APP_NAME}")
    
    # Sidebar para navegação
    page = st.sidebar.selectbox(
        "Navegação",
        ["Criar Livro", "Listar Livros", "Editar Livro", "Excluir Livro"]
    )
    
    # Renderizar página selecionada
    if page == "Criar Livro":
        create_book.render()
    elif page == "Listar Livros":
        list_books.render()
    elif page == "Editar Livro":
        edit_book.render()
    elif page == "Excluir Livro":
        delete_book.render()

if __name__ == "__main__":
    main() 