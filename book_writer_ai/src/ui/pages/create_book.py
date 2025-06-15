import streamlit as st
from src.ui.components.book_form import BookForm
from src.services.book_service import BookService

def render():
    st.header("Criar Novo Livro")
    
    book_service = BookService()
    
    # Campo de descrição
    description = st.text_area("Descrição do Livro (opcional)", height=150)
    
    if st.button("Gerar Sugestões"):
        if description:
            with st.spinner("Gerando sugestões..."):
                suggestions = book_service.generate_suggestions(description)
                if suggestions:
                    st.session_state.suggestions = suggestions
                else:
                    st.error("Não foi possível gerar sugestões. Tente novamente.")
    
    # Formulário com sugestões
    initial_data = st.session_state.get('suggestions', {})
    
    def handle_submit(book_data):
        book = book_service.create_book(book_data)
        if book:
            st.success("Livro salvo com sucesso!")
            st.session_state.suggestions = None
            st.experimental_rerun()
    
    BookForm(on_submit=handle_submit, initial_data=initial_data).render() 