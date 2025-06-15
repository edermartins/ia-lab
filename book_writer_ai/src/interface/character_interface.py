import streamlit as st
from src.services.character_service import CharacterService
from src.utils.logger import logger

class CharacterInterface:
    def __init__(self):
        logger.info("Inicializando CharacterInterface")
        self.service = CharacterService()
        logger.info("CharacterService inicializado com sucesso")

    def show_characters_list(self):
        st.header("Meus Personagens")
        characters = self.service.get_all_characters()
        if characters:
            for character in characters:
                with st.expander(f"👤 {character['nome']}"):
                    st.write(f"**Idade:** {character['idade']}")
                    st.write(f"**Papel:** {character['papel']}")
                    st.write(f"**Características Físicas:** {character['caracteristicas_fisicas']}")
                    st.write(f"**Personalidade:** {character['personalidade']}")
                    st.write(f"**Histórico:** {character['historico']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Editar", key=f"edit_char_{character['id']}"):
                            st.session_state['editing_character'] = character
                            st.rerun()
                    with col2:
                        if st.button("Excluir", key=f"delete_char_{character['id']}"):
                            try:
                                self.service.delete_character(character['id'])
                                st.success("Personagem excluído com sucesso!")
                                st.rerun()
                            except Exception as e:
                                logger.error(f"Erro ao excluir personagem: {str(e)}", exc_info=True)
                                st.error("Erro ao excluir personagem. Tente novamente.")
        else:
            st.info("Nenhum personagem cadastrado.") 