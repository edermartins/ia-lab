import os
from typing import Optional, Dict, Any
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

class LLMInterface:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")
        
        # Configuração do Google Gemini
        genai.configure(api_key=self.api_key)
        
        # Lista os modelos disponíveis
        try:
            models = genai.list_models()
            available_models = [model.name for model in models]
            print("Modelos disponíveis:", available_models)
            
            # Usa o modelo gemini-1.5-flash
            model_name = "models/gemini-1.5-flash"
            if model_name not in available_models:
                raise ValueError(f"Modelo {model_name} não está disponível. Modelos encontrados: {available_models}")
            
            self.model = genai.GenerativeModel(model_name)
            
            # Configuração do LangChain
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=self.api_key,
                temperature=0.7,
                convert_system_message_to_human=True
            )
            
        except Exception as e:
            raise ValueError(f"Erro ao configurar o modelo Gemini: {str(e)}")
        
        # Memória para conversas
        self.conversations: Dict[str, ConversationChain] = {}
    
    def get_conversation(self, conversation_id: str) -> ConversationChain:
        """Obtém ou cria uma nova conversa."""
        if conversation_id not in self.conversations:
            memory = ConversationBufferMemory()
            self.conversations[conversation_id] = ConversationChain(
                llm=self.llm,
                memory=memory,
                verbose=True
            )
        return self.conversations[conversation_id]
    
    async def generate_response(
        self,
        prompt: str,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Gera uma resposta do LLM."""
        try:
            if conversation_id:
                conversation = self.get_conversation(conversation_id)
                response = conversation.predict(input=prompt)
            else:
                # Configuração de segurança mais permissiva para criação de personagens
                safety_settings = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE"
                    }
                ]
                
                # Geração de conteúdo com configurações de segurança
                response = self.model.generate_content(
                    prompt,
                    safety_settings=safety_settings,
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.8,
                        "top_k": 40,
                    }
                )
                
                if response.prompt_feedback.block_reason:
                    raise ValueError(f"Conteúdo bloqueado: {response.prompt_feedback.block_reason}")
                
                response = response.text
            
            return response
        except Exception as e:
            error_msg = f"Erro ao gerar resposta: {str(e)}"
            print(error_msg)  # Log do erro no console
            return error_msg
    
    def clear_conversation(self, conversation_id: str) -> None:
        """Limpa uma conversa específica."""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
    
    def clear_all_conversations(self) -> None:
        """Limpa todas as conversas."""
        self.conversations.clear() 