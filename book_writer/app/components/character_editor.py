import streamlit as st
from typing import Dict, List
import json
import asyncio
from utils.llm_interface import LLMInterface
from utils.character_manager import CharacterManager

class CharacterEditor:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.character_manager = CharacterManager()
        
        # Inicializa as variáveis de estado se não existirem
        if "current_character" not in st.session_state:
            st.session_state.current_character = None
        if "physical_traits" not in st.session_state:
            st.session_state.physical_traits = ""
        if "personality" not in st.session_state:
            st.session_state.personality = ""
        if "background" not in st.session_state:
            st.session_state.background = ""
        if "character_name" not in st.session_state:
            st.session_state.character_name = ""
        if "character_age" not in st.session_state:
            st.session_state.character_age = 0
        if "character_role" not in st.session_state:
            st.session_state.character_role = "Protagonista"
        if "character_suggestions" not in st.session_state:
            st.session_state.character_suggestions = ""
        if "pending_character_data" not in st.session_state:
            st.session_state.pending_character_data = None
        if "should_update_character" not in st.session_state:
            st.session_state.should_update_character = False
    
    def render(self, story_id: str = None):
        """Renderiza o editor de personagens."""
        st.header("Editor de Personagens")
        
        if not story_id:
            st.warning("Por favor, selecione um livro primeiro.")
            return
        
        # Processa dados pendentes antes de qualquer renderização
        if st.session_state.pending_character_data:
            self._process_pending_character_data(story_id)
        
        # Sidebar para lista de personagens
        with st.sidebar:
            st.subheader("Personagens")
            
            # Botão para criar novo personagem
            if st.button("Novo Personagem"):
                st.session_state.character_name = ""
                st.session_state.character_age = 0
                st.session_state.character_role = "Protagonista"
                st.session_state.physical_traits = ""
                st.session_state.personality = ""
                st.session_state.background = ""
                st.session_state.character_suggestions = ""
                st.session_state.current_character = None
                st.session_state.character_chat = []  # Limpa o histórico de chat
                st.rerun()
            
            # Lista de personagens
            characters = self.character_manager.get_book_characters(story_id)
            if characters:
                for char_id, char in characters.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(f"👤 {char['name']}", key=f"char_{char_id}"):
                            st.session_state.current_character = char_id
                            st.session_state.character_chat = []
                            st.session_state.character_name = char.get("name", "")
                            st.session_state.character_age = char.get("age", 0)
                            st.session_state.character_role = char.get("role", "Protagonista")
                            st.session_state.physical_traits = char.get("physical_traits", "")
                            st.session_state.personality = char.get("personality", "")
                            st.session_state.background = char.get("background", "")
                            st.session_state.character_suggestions = char.get("suggestions", "")
                            st.rerun()
                    with col2:
                        if st.button("🗑️", key=f"delete_char_{char_id}"):
                            if self.character_manager.delete_character(char_id):
                                st.success(f"Personagem {char['name']} excluído com sucesso!")
                                if st.session_state.current_character == char_id:
                                    st.session_state.current_character = None
                                    st.session_state.character_name = ""
                                    st.session_state.character_age = 0
                                    st.session_state.character_role = "Protagonista"
                                    st.session_state.physical_traits = ""
                                    st.session_state.personality = ""
                                    st.session_state.background = ""
                                    st.session_state.character_suggestions = ""
                                    st.session_state.character_chat = []
                                st.rerun()
                            else:
                                st.error(f"Erro ao excluir personagem {char['name']}")
        
        # Área principal
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self._render_character_form(story_id)
        
        with col2:
            if st.session_state.current_character:
                asyncio.run(self._render_character_chat())
            else:
                st.info("Selecione um personagem na barra lateral ou crie um novo para começar a conversar.")
    
    def _render_character_form(self, story_id: str):
        """Renderiza o formulário de edição do personagem."""
        with st.form("character_form", clear_on_submit=False):
            st.subheader("Detalhes do Personagem")
            
            # Campos do formulário
            name = st.text_input("Nome", value=st.session_state.character_name, key="character_name")
            age = st.number_input("Idade", min_value=0, max_value=120, key="character_age")
            role = st.selectbox(
                "Papel na História",
                ["Protagonista", "Antagonista", "Coadjuvante", "Figurante"],
                index=["Protagonista", "Antagonista", "Coadjuvante", "Figurante"].index(st.session_state.character_role),
                key="character_role"
            )
            
            # Campo de sugestões
            suggestions = st.text_area(
                "Sugestões para o Personagem (opcional)",
                value=st.session_state.character_suggestions,
                help="Digite sugestões ou ideias para a criação do personagem. Deixe em branco para geração automática.",
                key="character_suggestions"
            )
            
            # Campos de texto para características
            physical_traits = st.text_area(
                "Características Físicas",
                value=st.session_state.physical_traits,
                key="physical_traits"
            )
            personality = st.text_area(
                "Personalidade",
                value=st.session_state.personality,
                key="personality"
            )
            background = st.text_area(
                "Histórico",
                value=st.session_state.background,
                key="background"
            )
            
            # Botões de ação
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Salvar Personagem"):
                    character_data = {
                        "name": name,
                        "age": age,
                        "role": role,
                        "physical_traits": physical_traits,
                        "personality": personality,
                        "background": background,
                        "suggestions": suggestions,
                        "story_id": story_id
                    }
                    self._save_character(character_data)
            
            with col2:
                if st.form_submit_button("Gerar com IA"):
                    asyncio.run(self._generate_character_details(name, role))
    
    async def _render_character_chat(self):
        st.subheader("Chat com o Personagem")
        
        # Área de chat
        if "character_chat" not in st.session_state:
            st.session_state.character_chat = []
        
        # Exibir mensagens do chat
        for msg in st.session_state.character_chat:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # Input para nova mensagem
        if prompt := st.chat_input("Converse com o personagem..."):
            # Adicionar mensagem do usuário
            st.session_state.character_chat.append({
                "role": "user",
                "content": prompt
            })
            
            # Gerar resposta do personagem
            character = self._get_current_character_context()
            if not character:
                st.warning("Por favor, selecione um personagem primeiro.")
                return
            
            # Criar prompt contextualizado
            character_prompt = f"""
            Você é {character['name']}, um personagem com as seguintes características:
            
            Aparência: {character.get('physical_traits', 'Não especificado')}
            Personalidade: {character.get('personality', 'Não especificado')}
            Histórico: {character.get('background', 'Não especificado')}
            
            Responda à seguinte mensagem como se fosse este personagem, mantendo sua personalidade e características:
            
            {prompt}
            
            IMPORTANTE: Responda diretamente como o personagem, sem explicar que você é o personagem ou adicionar qualquer texto adicional.
            """
            
            response = await self.llm.generate_response(
                prompt=character_prompt,
                conversation_id="character_chat"
            )
            
            # Adicionar resposta do personagem
            st.session_state.character_chat.append({
                "role": "assistant",
                "content": response
            })
            
            # Atualizar a interface
            st.rerun()
    
    async def _generate_character_details(self, name: str, role: str):
        """Gera detalhes do personagem usando IA."""
        if not name:
            st.warning("Por favor, insira um nome para o personagem.")
            return
        
        # Obtém as sugestões do session_state
        suggestions = st.session_state.character_suggestions
        
        # Prepara o prompt base
        prompt = f"""
        Crie um perfil detalhado e apropriado para um personagem de livro com as seguintes informações:
        Nome: {name}
        Papel: {role}
        """
        
        # Adiciona as sugestões ao prompt se existirem
        if suggestions:
            prompt += f"""
            Sugestões e ideias para o personagem:
            {suggestions}
            """
        
        prompt += """
        Por favor, forneça um perfil profissional e adequado com:
        1. Descrição física detalhada (aparência, estilo, características distintivas)
        2. Traços de personalidade (comportamento, valores, atitudes)
        3. Histórico e motivações (origem, objetivos, experiências passadas)
        
        IMPORTANTE: A resposta DEVE ser um JSON válido com exatamente estas chaves:
        {
            "physical_traits": "descrição física aqui",
            "personality": "traços de personalidade aqui",
            "background": "histórico e motivações aqui"
        }
        
        Mantenha o conteúdo apropriado e profissional. Não inclua nenhum texto adicional antes ou depois do JSON.
        """
        
        try:
            response = await self.llm.generate_response(prompt)
            
            # Tenta limpar a resposta caso contenha markdown ou outros caracteres
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            details = json.loads(response)
            
            # Verifica se todas as chaves necessárias estão presentes
            required_keys = ["physical_traits", "personality", "background"]
            if not all(key in details for key in required_keys):
                st.error(f"Resposta incompleta. Chaves esperadas: {required_keys}")
                st.write("Resposta recebida:", details)
                return
            
            # Cria o personagem com os detalhes gerados
            character_data = {
                "name": name,
                "role": role,
                "physical_traits": details["physical_traits"],
                "personality": details["personality"],
                "background": details["background"],
                "suggestions": suggestions
            }
            
            # Armazena os dados para processamento após a renderização
            st.session_state.pending_character_data = character_data
            st.success(f"Personagem {name} gerado com sucesso!")
            st.rerun()
            
        except json.JSONDecodeError as e:
            st.error(f"Erro ao processar a resposta da IA: {str(e)}")
            st.write("Resposta que causou o erro:", response)
        except Exception as e:
            st.error(f"Erro inesperado: {str(e)}")
            st.write("Resposta que causou o erro:", response)
    
    def _save_character(self, character_data: Dict):
        """Salva os dados do personagem."""
        if not character_data.get("name"):
            st.warning("O nome do personagem é obrigatório.")
            return
            
        # Armazena os dados para processamento após a renderização
        st.session_state.pending_character_data = character_data
        st.success(f"Personagem {character_data['name']} salvo com sucesso!")
        st.rerun()
    
    def _get_current_character_context(self) -> Dict:
        """Retorna o contexto do personagem atual para o chat."""
        if hasattr(st.session_state, "current_character"):
            char_id = st.session_state.current_character
            if char_id:
                return self.character_manager.get_character(char_id)
        return {}

    def _process_pending_character_data(self, story_id: str):
        """Processa os dados do personagem pendentes após a renderização."""
        data = st.session_state.pending_character_data
        if not data:
            return
            
        char_id = self.character_manager.save_character(data)
        st.session_state.current_character = char_id
        st.session_state.character_name = data.get("name", "")
        st.session_state.character_role = data.get("role", "Protagonista")
        st.session_state.physical_traits = data.get("physical_traits", "")
        st.session_state.personality = data.get("personality", "")
        st.session_state.background = data.get("background", "")
        st.session_state.character_suggestions = data.get("suggestions", "")
        st.session_state.pending_character_data = None 