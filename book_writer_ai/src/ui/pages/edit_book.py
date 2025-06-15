import streamlit as st
from src.ui.components.book_form import BookForm
from src.services.book_service import BookService

def render():
    st.header("Editar Livro")
    
    book_service = BookService()
    books = book_service.get_all_books()
    
    if not books:
        st.info("Nenhum livro cadastrado para editar.")
    else:
        book_to_edit = st.selectbox(
            "Selecione o livro para editar",
            books,
            format_func=lambda x: f"{x.titulo} - Volume {x.volume}"
        )
        
        if book_to_edit:
            def handle_submit(book_data):
                updated_book = book_service.update_book(book_to_edit.id, book_data)
                if updated_book:
                    st.success("Livro atualizado com sucesso!")
                    st.experimental_rerun()
            
            BookForm(
                on_submit=handle_submit,
                initial_data=book_to_edit.to_dict()
            ).render() 