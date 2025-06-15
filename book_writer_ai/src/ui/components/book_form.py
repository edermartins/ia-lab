import streamlit as st
from typing import Dict, Optional, Callable

class BookForm:
    def __init__(self, on_submit: Callable, initial_data: Optional[Dict] = None):
        self.on_submit = on_submit
        self.initial_data = initial_data or {}
    
    def render(self):
        """Renderiza o formulário de livro."""
        with st.form("book_form"):
            titulo = st.text_input("Título", value=self.initial_data.get("titulo", ""))
            volume = st.text_input("Volume", value=self.initial_data.get("volume", ""))
            autor = st.text_input("Autor", value=self.initial_data.get("autor", ""))
            genero = st.text_input("Gênero", value=self.initial_data.get("genero", ""))
            idioma = st.text_input("Idioma", value=self.initial_data.get("idioma", ""))
            
            submitted = st.form_submit_button("Salvar")
            
            if submitted:
                if all([titulo, volume, autor, genero, idioma]):
                    self.on_submit({
                        "titulo": titulo,
                        "volume": volume,
                        "autor": autor,
                        "genero": genero,
                        "idioma": idioma
                    })
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios.") 