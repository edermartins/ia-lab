import streamlit as st
from src.services.book_service import BookService

def render():
    st.header("Excluir Livro")
    
    book_service = BookService()
    books = book_service.get_all_books()
    
    if not books:
        st.info("Nenhum livro cadastrado para excluir.")
    else:
        book_to_delete = st.selectbox(
            "Selecione o livro para excluir",
            books,
            format_func=lambda x: f"{x.titulo} - Volume {x.volume}"
        )
        
        if book_to_delete and st.button("Excluir Livro"):
            if book_service.delete_book(book_to_delete.id):
                st.success("Livro excluído com sucesso!")
                st.experimental_rerun() 