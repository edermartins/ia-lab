import os
import json
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from src.utils.logger import logger

class CharacterSuggestion(BaseModel):
    nome: str = Field(description="Nome do personagem")
    idade: int = Field(description="Idade do personagem")
    papel: str = Field(description="Papel do personagem na história")
    caracteristicas_fisicas: str = Field(description="Descrição física do personagem")
    personalidade: str = Field(description="Traços de personalidade")
    historico: str = Field(description="Histórico e background do personagem")

class CharacterSuggestionList(BaseModel):
    suggestions: List[CharacterSuggestion] = Field(description="Lista de sugestões de personagens")

class CharacterSuggestionAgent:
    def __init__(self):
        """Inicializa o agente de sugestões de personagens."""
        logger.info("Inicializando CharacterSuggestionAgent")
        
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
        self.parser = PydanticOutputParser(pydantic_object=CharacterSuggestionList)
        
        # Configurar o template do prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um escritor e roteirista especializado na criação de detalhes de personagens. 
             Com base na descrição fornecida, crie uma sugestão detalhada de personagem com bastante criatividade,
             seguindo as sugestões antes das Regras importantes. Se não houver sugestões, crie um personagem com 
             criatividade.
            
            {format_instructions}
            
            Regras importantes:
            1. Use aspas duplas para strings
            2. Não use vírgula após o último item
            3. Não inclua texto adicional ou formatação markdown
            4. Não use blocos de código
            5. Retorne apenas o JSON válido"""),
            ("human", "Descrição: {description}")
        ])
        
        logger.info("CharacterSuggestionAgent inicializado com sucesso")
    
    def generate_suggestions(self, description: str) -> List[Dict[str, Any]]:
        """
        Gera sugestões de personagens com base na descrição fornecida.
        
        Args:
            description (str): Descrição do personagem desejado
            
        Returns:
            List[Dict[str, Any]]: Lista de sugestões de personagens
        """
        logger.info(f"Gerando sugestões para descrição: {description[:100]}...")
        
        try:
            # Preparar o prompt com as instruções de formato
            prompt = self.prompt.format_messages(
                description=description,
                format_instructions=self.parser.get_format_instructions()
            )
            
            # Salva a resposta
            response = self.model.invoke(prompt)
            
            # Log da resposta bruta (deu muito erro antes de dar certo)
            logger.info(f"Resposta bruta recebida: {response.content[:200]}...")
            
            # Parser da resposta
            result = self.parser.parse(response.content)
            
            # Converte para dict
            suggestions = [suggestion.dict() for suggestion in result.suggestions]
            
            logger.info(f"Retornando {len(suggestions)} sugestões válidas")
            return suggestions
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões: {str(e)}", exc_info=True)
            return [] 