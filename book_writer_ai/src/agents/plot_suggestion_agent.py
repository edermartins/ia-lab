import os
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from src.utils.logger import logger

class PlotSuggestion(BaseModel):
    titulo: str = Field(description="Título do livro")
    volume: str = Field(description="Número do volume (se aplicável)")
    autor: str = Field(description="Nome do autor")
    genero: str = Field(description="Gênero literário")
    idioma: str = Field(description="Idioma do livro")
    sinopse: str = Field(description="Breve descrição do enredo")
    estilo_narrativo: str = Field(description="Estilo de narração (ex: primeira pessoa, terceira pessoa, epistolar, etc.)")
    publico_alvo: str = Field(description="Público alvo do livro (ex: infantil, juvenil, adulto, etc.)")

class PlotSuggestionList(BaseModel):
    suggestions: List[PlotSuggestion] = Field(description="Lista de sugestões de enredo")

class PlotSuggestionAgent:
    def __init__(self):
        """Inicializa o agente de sugestões de enredo."""
        logger.info("Inicializando PlotSuggestionAgent")
        
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
            max_output_tokens=2048
        )
        
        # Configurar o parser de saída
        self.parser = PydanticOutputParser(pydantic_object=PlotSuggestionList)
        
        # Configurar o template do prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um escritor e roteirista especializado em criar enredos complexos e empolgantes. 
             Com base na descrição fornecida abaixo, crie uma sugestão detalhada de enredo. Caso não haja sugestões, entre
             esta linha e Regras importantes, crie um enredo com bastante criatividade.
            
            {format_instructions}
            
            Regras importantes:
            1. Use aspas duplas para strings
            2. Não use vírgula após o último item
            3. Não inclua texto adicional ou formatação markdown
            4. Não use blocos de código
            5. Retorne apenas o JSON válido"""),
            ("human", "Descrição: {description}")
        ])
        
        logger.info("PlotSuggestionAgent inicializado com sucesso")
    
    def generate_suggestions(self, description: str) -> List[Dict[str, Any]]:
        """
        Gera sugestões de enredo com base na descrição fornecida.
        
        Args:
            description (str): Descrição do enredo desejado
            
        Returns:
            List[Dict[str, Any]]: Lista de sugestões de enredo
        """
        logger.info(f"Gerando sugestões para descrição: {description[:100]}...")
        
        try:
            # Prepara o prompt com as instruções de formatação
            prompt = self.prompt.format_messages(
                description=description,
                format_instructions=self.parser.get_format_instructions()
            )
            
            # Gera a resposta
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