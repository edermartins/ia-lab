import streamlit as st
from typing import Dict, List
import json
import asyncio
from utils.llm_interface import LLMInterface
from utils.environment_manager import EnvironmentManager
import uuid

class EnvironmentEditor:
    def __init__(self, llm: LLMInterface):
        self.llm = llm
        self.environment_manager = EnvironmentManager()
        
        # Inicializa as variáveis de estado se não existirem
        if 'environment_name' not in st.session_state:
            st.session_state.environment_name = ""
        if 'environment_type' not in st.session_state:
            st.session_state.environment_type = ""
        if 'physical_description' not in st.session_state:
            st.session_state.physical_description = ""
        if 'atmosphere' not in st.session_state:
            st.session_state.atmosphere = ""
        if 'important_elements' not in st.session_state:
            st.session_state.important_elements = ""
        if 'significance' not in st.session_state:
            st.session_state.significance = ""
        if 'environment_suggestions' not in st.session_state:
            st.session_state.environment_suggestions = ""
        if 'selected_environment' not in st.session_state:
            st.session_state.selected_environment = None
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'pending_chat_message' not in st.session_state:
            st.session_state.pending_chat_message = None
        if 'pending_environment_data' not in st.session_state:
            st.session_state.pending_environment_data = None
    
    def render(self, story_id: str = None):
        """Renderiza o editor de ambientes."""
        st.header("Editor de Ambientes")
        
        if not story_id:
            st.warning("Por favor, selecione um livro primeiro.")
            return
        
        # Processa dados pendentes antes de qualquer renderização
        if st.session_state.pending_environment_data:
            self._process_pending_environment_data(story_id)
        
        # Sidebar para lista de ambientes
        with st.sidebar:
            st.subheader("Ambientes")
            
            # Botão para criar novo ambiente
            if st.button("Novo Ambiente"):
                st.session_state.environment_name = ""
                st.session_state.environment_type = ""
                st.session_state.physical_description = ""
                st.session_state.atmosphere = ""
                st.session_state.important_elements = ""
                st.session_state.significance = ""
                st.session_state.environment_suggestions = ""
                st.session_state.current_environment = None
                st.rerun()
            
            # Lista de ambientes
            environments = self.environment_manager.get_book_environments(story_id)
            if environments:
                for env_id, env in environments.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(f"🏠 {env['name']}", key=f"env_{env_id}"):
                            st.session_state.current_environment = env_id
                            st.session_state.environment_name = env.get("name", "")
                            st.session_state.environment_type = env.get("type", "")
                            st.session_state.physical_description = env.get("physical_description", "")
                            st.session_state.atmosphere = env.get("atmosphere", "")
                            st.session_state.important_elements = env.get("important_elements", "")
                            st.session_state.significance = env.get("significance", "")
                            st.session_state.environment_suggestions = env.get("suggestions", "")
                            st.rerun()
                    with col2:
                        if st.button("🗑️", key=f"delete_env_{env_id}"):
                            if self.environment_manager.delete_environment(env_id):
                                st.success(f"Ambiente {env['name']} excluído com sucesso!")
                                if st.session_state.current_environment == env_id:
                                    st.session_state.current_environment = None
                                    st.session_state.environment_name = ""
                                    st.session_state.environment_type = ""
                                    st.session_state.physical_description = ""
                                    st.session_state.atmosphere = ""
                                    st.session_state.important_elements = ""
                                    st.session_state.significance = ""
                                    st.session_state.environment_suggestions = ""
                                st.rerun()
                            else:
                                st.error(f"Erro ao excluir ambiente {env['name']}")
        
        # Área principal
        self._render_environment_form(story_id)
    
    def _render_environment_form(self, story_id: str):
        """Renderiza o formulário de edição do ambiente."""
        with st.form("environment_form", clear_on_submit=False):
            st.subheader("Detalhes do Ambiente")
            
            # Campos do formulário
            name = st.text_input("Nome", value=st.session_state.environment_name, key="environment_name")
            env_type = st.text_input("Tipo", value=st.session_state.environment_type, key="environment_type")
            
            # Campo de sugestões
            suggestions = st.text_area(
                "Sugestões para o Ambiente (opcional)",
                value=st.session_state.environment_suggestions,
                help="Digite sugestões ou ideias para a criação do ambiente. Deixe em branco para geração automática.",
                key="environment_suggestions"
            )
            
            # Campos de texto para características
            physical_description = st.text_area(
                "Descrição Física",
                value=st.session_state.physical_description,
                key="physical_description"
            )
            atmosphere = st.text_area(
                "Atmosfera",
                value=st.session_state.atmosphere,
                key="atmosphere"
            )
            important_elements = st.text_area(
                "Elementos Importantes",
                value=st.session_state.important_elements,
                key="important_elements"
            )
            significance = st.text_area(
                "Significado",
                value=st.session_state.significance,
                key="significance"
            )
            
            # Botões de ação
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Salvar Ambiente"):
                    environment_data = {
                        "name": name,
                        "type": env_type,
                        "physical_description": physical_description,
                        "atmosphere": atmosphere,
                        "important_elements": important_elements,
                        "significance": significance,
                        "suggestions": suggestions,
                        "story_id": story_id
                    }
                    self._save_environment(environment_data)
            
            with col2:
                if st.form_submit_button("Gerar com IA"):
                    asyncio.run(self._generate_environment_details(name, env_type))
    
    def _save_environment(self, environment_data: Dict):
        """Salva os dados do ambiente."""
        if not environment_data.get("name"):
            st.warning("O nome do ambiente é obrigatório.")
            return
            
        # Armazena os dados para processamento após a renderização
        st.session_state.pending_environment_data = environment_data
        st.success(f"Ambiente {environment_data['name']} salvo com sucesso!")
        st.rerun()
    
    def _process_pending_environment_data(self, story_id: str):
        """Processa os dados do ambiente pendentes após a renderização."""
        data = st.session_state.pending_environment_data
        if not data:
            return
            
        env_id = self.environment_manager.save_environment(data)
        st.session_state.current_environment = env_id
        st.session_state.environment_name = data.get("name", "")
        st.session_state.environment_type = data.get("type", "")
        st.session_state.physical_description = data.get("physical_description", "")
        st.session_state.atmosphere = data.get("atmosphere", "")
        st.session_state.important_elements = data.get("important_elements", "")
        st.session_state.significance = data.get("significance", "")
        st.session_state.environment_suggestions = data.get("suggestions", "")
        st.session_state.pending_environment_data = None
    
    def _handle_generate_ia(self, name: str, type: str):
        """Manipula a geração de ambiente com IA de forma síncrona."""
        if not name:
            st.warning("Por favor, insira um nome para o ambiente.")
            return
        
        # Obtém as sugestões do session_state
        suggestions = st.session_state.environment_suggestions
        
        # Prepara o prompt base
        prompt = f"""
        Crie uma descrição detalhada para um ambiente de livro com as seguintes informações:
        Nome: {name}
        Tipo: {type}
        """
        
        # Adiciona as sugestões ao prompt se existirem
        if suggestions:
            prompt += f"""
            Sugestões e ideias para o ambiente:
            {suggestions}
            """
        
        prompt += """
        Por favor, forneça:
        1. Descrição física detalhada
        2. Atmosfera e clima
        3. Elementos importantes
        4. Significado na história
        
        IMPORTANTE: A resposta DEVE ser um JSON válido com exatamente estas chaves:
        {
            "physical_description": "descrição física aqui",
            "atmosphere": "atmosfera e clima aqui",
            "important_elements": "elementos importantes aqui",
            "significance": "significado na história aqui"
        }
        
        Mantenha o conteúdo apropriado e profissional. Não inclua nenhum texto adicional antes ou depois do JSON.
        """
        
        try:
            # Cria um novo loop de eventos
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Executa a geração de forma síncrona
            response = loop.run_until_complete(self.llm.generate_response(prompt))
            
            # Debug: mostra a resposta recebida
            st.write("Resposta recebida da IA:", response)
            
            # Tenta limpar a resposta caso contenha markdown ou outros caracteres
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            # Debug: mostra a resposta limpa
            st.write("Resposta limpa:", response)
            
            details = json.loads(response)
            
            # Verifica se todas as chaves necessárias estão presentes
            required_keys = ["physical_description", "atmosphere", "important_elements", "significance"]
            if not all(key in details for key in required_keys):
                missing_keys = [key for key in required_keys if key not in details]
                st.error(f"Resposta incompleta. Chaves faltando: {missing_keys}")
                st.write("Resposta recebida:", details)
                return
            
            # Cria o objeto de ambiente com os dados gerados
            environment_data = {
                "name": name,
                "type": type,
                "physical_description": details["physical_description"],
                "atmosphere": details["atmosphere"],
                "important_elements": details["important_elements"],
                "significance": details["significance"],
                "suggestions": suggestions
            }
            
            # Armazena os dados para processamento após a renderização
            st.session_state.pending_environment_data = environment_data
            st.success("Detalhes do ambiente gerados com sucesso!")
            st.rerun()
            
        except json.JSONDecodeError as e:
            st.error(f"Erro ao processar a resposta da IA: {str(e)}")
            st.write("Resposta que causou o erro:", response)
        except Exception as e:
            st.error(f"Erro ao gerar detalhes do ambiente: {str(e)}")
            st.write("Resposta que causou o erro:", response)
        finally:
            # Limpa o loop de eventos
            loop.close()
    
    async def _render_environment_chat(self):
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
            environment = self._get_current_environment_context()
            if not environment:
                st.warning("Por favor, selecione um ambiente primeiro.")
                return
            
            # Criar prompt contextualizado
            environment_prompt = f"""
            Você é o ambiente '{environment['name']}' em uma história. Responda à seguinte mensagem como se fosse este ambiente:
            
            Detalhes do ambiente:
            - Tipo: {environment['type']}
            - Descrição Física: {environment['physical_description']}
            - Atmosfera: {environment['atmosphere']}
            - Elementos Importantes: {environment['important_elements']}
            - Significado: {environment['significance']}
            
            Responda à seguinte mensagem como se fosse este ambiente, mantendo suas características e atmosfera:
            
            {prompt}
            
            IMPORTANTE: Responda diretamente como o ambiente, sem explicar que você é o ambiente ou adicionar qualquer texto adicional.
            """
            
            response = await self.llm.generate_response(
                prompt=environment_prompt,
                conversation_id="environment_chat"
            )
            
            # Adicionar resposta do ambiente
            st.session_state.environment_chat.append({
                "role": "assistant",
                "content": response
            })
            
            # Atualizar a interface
            st.rerun()
    
    def _get_current_environment_context(self) -> Dict:
        """Retorna o contexto do ambiente atual para o chat."""
        if st.session_state.selected_environment:
            return self.environment_manager.get_environment(st.session_state.selected_environment)
        return {}

    def _process_pending_chat_message(self):
        """Processa uma mensagem de chat pendente."""
        if st.session_state.pending_chat_message:
            message = st.session_state.pending_chat_message
            st.session_state.pending_chat_message = None
            
            # Obtém os detalhes do ambiente
            environment = self._get_current_environment_context()
            if not environment:
                st.error("Ambiente não encontrado.")
                return
            
            # Prepara o prompt para o chat
            prompt = f"""
            Você é o ambiente '{environment['name']}' em uma história. Responda à seguinte mensagem como se fosse este ambiente:
            
            Detalhes do ambiente:
            - Tipo: {environment['type']}
            - Descrição Física: {environment['physical_description']}
            - Atmosfera: {environment['atmosphere']}
            - Elementos Importantes: {environment['important_elements']}
            - Significado: {environment['significance']}
            
            Mensagem do usuário: {message}
            
            Responda de forma imersiva e coerente com a natureza do ambiente.
            """
            
            try:
                # Cria um novo loop de eventos
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Executa a geração de forma síncrona
                response = loop.run_until_complete(self.llm.generate_response(prompt))
                
                # Atualiza o histórico de chat
                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []
                
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": message
                })
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Limpa a mensagem do usuário
                st.session_state.user_message = ""
                
            except Exception as e:
                st.error(f"Erro ao processar a mensagem: {str(e)}")
            finally:
                # Limpa o loop de eventos
                loop.close() 