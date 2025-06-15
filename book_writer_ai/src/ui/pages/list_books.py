import streamlit as st
from src.services.book_service import BookService

def render():
    st.header("Lista de Livros")
    
    book_service = BookService()
    books = book_service.get_all_books()
    
    if not books:
        st.info("Nenhum livro cadastrado.")
    else:
        for book in books:
            with st.expander(f"{book.titulo} - Volume {book.volume}"):
                st.write(f"**Autor:** {book.autor}")
                st.write(f"**Gênero:** {book.genero}")
                st.write(f"**Idioma:** {book.idioma}")
                st.write(f"**ID:** {book.id}")
                st.write(f"**Criado em:** {book.created_at.strftime('%d/%m/%Y %H:%M')}")
                st.write(f"**Atualizado em:** {book.updated_at.strftime('%d/%m/%Y %H:%M')}") 