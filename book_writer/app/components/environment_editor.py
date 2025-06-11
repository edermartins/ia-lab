import streamlit as st
from typing import Dict, List
import json
from utils.llm_interface import LLMInterface

class EnvironmentEditor:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        
        # Carregar ambientes existentes
        if "environments" not in st.session_state:
            st.session_state.environments = {}
    
    def render(self):
        st.header("Editor de Ambientes")
        
        # Sidebar para lista de ambientes
        with st.sidebar:
            st.subheader("Ambientes")
            if st.button("Novo Ambiente"):
                st.session_state.current_environment = None
            
            for env_id, env in st.session_state.environments.items():
                if st.button(f"🏞️ {env['name']}", key=f"env_{env_id}"):
                    st.session_state.current_environment = env_id
        
        # Área principal
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self._render_environment_form()
        
        with col2:
            self._render_environment_chat()
    
    def _render_environment_form(self):
        st.subheader("Detalhes do Ambiente")
        
        # Formulário de ambiente
        name = st.text_input("Nome do Ambiente")
        type = st.selectbox(
            "Tipo de Ambiente",
            ["Interior", "Exterior", "Fantástico", "Futurista", "Histórico"]
        )
        
        # Descrição física
        st.subheader("Descrição Física")
        physical_description = st.text_area(
            "Descrição do Ambiente",
            height=150,
            help="Descreva a aparência física do ambiente"
        )
        
        # Atmosfera
        st.subheader("Atmosfera")
        atmosphere = st.text_area(
            "Atmosfera e Clima",
            height=100,
            help="Descreva a atmosfera e o clima do ambiente"
        )
        
        # Elementos importantes
        st.subheader("Elementos Importantes")
        important_elements = st.text_area(
            "Elementos e Objetos",
            height=100,
            help="Liste os elementos e objetos importantes do ambiente"
        )
        
        # Significado
        st.subheader("Significado na História")
        significance = st.text_area(
            "Importância do Ambiente",
            height=100,
            help="Descreva a importância deste ambiente na história"
        )
        
        # Botões de ação
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Salvar Ambiente"):
                self._save_environment({
                    "name": name,
                    "type": type,
                    "physical_description": physical_description,
                    "atmosphere": atmosphere,
                    "important_elements": important_elements,
                    "significance": significance
                })
        
        with col2:
            if st.button("Gerar com IA"):
                self._generate_environment_details(name, type)
    
    def _render_environment_chat(self):
        st.subheader("Chat com o Ambiente")
        
        # Área de chat
        if "environment_chat" not in st.session_state:
            st.session_state.environment_chat = []
        
        # Exibir mensagens do chat
        for msg in st.session_state.environment_chat:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # Input para nova mensagem
        if prompt := st.chat_input("Converse sobre o ambiente..."):
            # Adicionar mensagem do usuário
            st.session_state.environment_chat.append({
                "role": "user",
                "content": prompt
            })
            
            # Gerar resposta do ambiente
            environment_context = self._get_current_environment_context()
            response = self.llm.generate_response(
                prompt=prompt,
                conversation_id="environment_chat",
                context=environment_context
            )
            
            # Adicionar resposta do ambiente
            st.session_state.environment_chat.append({
                "role": "assistant",
                "content": response
            })
            
            # Atualizar a interface
            st.experimental_rerun()
    
    def _save_environment(self, environment_data: Dict):
        """Salva os dados do ambiente."""
        if environment_data["name"]:
            env_id = environment_data["name"].lower().replace(" ", "_")
            st.session_state.environments[env_id] = environment_data
            st.success(f"Ambiente {environment_data['name']} salvo com sucesso!")
    
    def _generate_environment_details(self, name: str, type: str):
        """Gera detalhes do ambiente usando IA."""
        if not name:
            st.warning("Por favor, insira um nome para o ambiente.")
            return
        
        prompt = f"""
        Crie uma descrição detalhada para um ambiente de livro com as seguintes informações:
        Nome: {name}
        Tipo: {type}
        
        Por favor, forneça:
        1. Descrição física detalhada
        2. Atmosfera e clima
        3. Elementos importantes
        4. Significado na história
        
        Formate a resposta em JSON com as chaves: physical_description, atmosphere, important_elements, significance
        """
        
        response = self.llm.generate_response(prompt)
        try:
            details = json.loads(response)
            st.session_state.environment_details = details
            st.success("Detalhes do ambiente gerados com sucesso!")
        except json.JSONDecodeError:
            st.error("Erro ao processar a resposta da IA")
    
    def _get_current_environment_context(self) -> Dict:
        """Retorna o contexto do ambiente atual para o chat."""
        if hasattr(st.session_state, "current_environment"):
            env_id = st.session_state.current_environment
            if env_id in st.session_state.environments:
                return st.session_state.environments[env_id]
        return {} 