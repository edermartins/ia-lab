import streamlit as st
from src.services.environment_service import EnvironmentService
from src.utils.logger import logger

class EnvironmentInterface:
    def __init__(self):
        logger.info("Inicializando EnvironmentInterface")
        self.service = EnvironmentService()
        logger.info("EnvironmentService inicializado com sucesso")

    def show_environments_list(self):
        st.header("Meus Ambientes")
        environments = self.service.get_all_environments()
        if environments:
            for environment in environments:
                with st.expander(f"🌍 {environment['nome']}"):
                    st.write(f"**Tipo:** {environment['tipo']}")
                    st.write(f"**Descrição:** {environment['descricao']}")
                    st.write(f"**Atmosfera:** {environment['atmosfera']}")
                    st.write(f"**Elementos Importantes:** {environment['elementos_importantes']}")
                    st.write(f"**Significado:** {environment['significado']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Editar", key=f"edit_env_{environment['id']}"):
                            st.session_state['editing_environment'] = environment
                            st.rerun()
                    with col2:
                        if st.button("Excluir", key=f"delete_env_{environment['id']}"):
                            try:
                                self.service.delete_environment(environment['id'])
                                st.success("Ambiente excluído com sucesso!")
                                st.rerun()
                            except Exception as e:
                                logger.error(f"Erro ao excluir ambiente: {str(e)}", exc_info=True)
                                st.error("Erro ao excluir ambiente. Tente novamente.")
        else:
            st.info("Nenhum ambiente cadastrado.") 