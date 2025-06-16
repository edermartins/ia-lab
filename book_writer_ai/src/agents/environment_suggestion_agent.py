import os
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from src.utils.logger import logger

class EnvironmentSuggestion(BaseModel):
    nome: str = Field(description="Nome do ambiente")
    tipo: str = Field(description="Tipo de ambiente (ex: floresta, cidade, castelo, etc.)")
    descricao: str = Field(description="Descrição detalhada do ambiente")
    atmosfera: str = Field(description="Atmosfera e clima do ambiente")
    elementos_importantes: str = Field(description="Elementos e objetos importantes no ambiente")
    significado: str = Field(description="Significado simbólico ou importância do ambiente na história")

class EnvironmentSuggestionList(BaseModel):
    suggestions: List[EnvironmentSuggestion] = Field(description="Lista de sugestões de ambientes")

class EnvironmentSuggestionAgent:
    def __init__(self):
        """Inicializa o agente de sugestões de ambientes."""
        logger.info("Inicializando EnvironmentSuggestionAgent")
        
        # Configurar a API do Google
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")
        
        # Inicializar o modelo LangChain
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0.7,
            top_p=0.8,
            top_k=40,
            max_output_tokens=2048,
            convert_system_message_to_human=True
        )
        
        # Configurar o parser de saída
        self.parser = PydanticOutputParser(pydantic_object=EnvironmentSuggestionList)
        
        # Configurar o template do prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um escritor e roteirista especializado em criar ambientes e cenários. 
            Com base na descrição fornecida, crie uma sugestão detalhada de ambiente com um bom nível de detalhes e criatividade.
            
            {format_instructions}
            
            Regras importantes:
            1. Use aspas duplas para strings
            2. Não use vírgula após o último item
            3. Não inclua texto adicional ou formatação markdown
            4. Não use blocos de código
            5. Retorne apenas o JSON válido"""),
            ("human", "Descrição: {description}")
        ])
        
        logger.info("EnvironmentSuggestionAgent inicializado com sucesso")
    
    def generate_suggestions(self, description: str) -> List[Dict[str, Any]]:
        """
        Gera sugestões de ambientes com base na descrição fornecida.
        
        Args:
            description (str): Descrição do ambiente desejado
            
        Returns:
            List[Dict[str, Any]]: Lista de sugestões de ambientes
        """
        logger.info(f"Gerando sugestões para descrição: {description[:100]}...")
        
        try:
            # Preparar o prompt com as instruções de formato
            prompt = self.prompt.format_messages(
                description=description,
                format_instructions=self.parser.get_format_instructions()
            )
            
            # Gerar a resposta
            response = self.model.invoke(prompt)
            
            # Log da resposta bruta
            logger.info(f"Resposta bruta recebida: {response.content[:200]}...")
            
            # Parsear a resposta
            result = self.parser.parse(response.content)
            
            # Converter para lista de dicionários
            suggestions = [suggestion.dict() for suggestion in result.suggestions]
            
            logger.info(f"Retornando {len(suggestions)} sugestões válidas")
            return suggestions
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões: {str(e)}", exc_info=True)
            return [] 