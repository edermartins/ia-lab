import os
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from src.utils.logger import logger

class BookSuggestion(BaseModel):
    titulo: str = Field(description="Título do livro")
    volume: str = Field(description="Número do volume (se aplicável)")
    autor: str = Field(description="Nome do autor")
    genero: str = Field(description="Gênero literário")
    idioma: str = Field(description="Idioma do livro")
    sinopse: str = Field(description="Breve descrição do enredo")
    estilo_narrativo: str = Field(description="Estilo de narração (ex: primeira pessoa, terceira pessoa, epistolar, etc.)")
    publico_alvo: str = Field(description="Público alvo do livro (ex: infantil, juvenil, adulto, etc.)")

class BookSuggestionList(BaseModel):
    suggestions: List[BookSuggestion] = Field(description="Lista de sugestões de livros")

class BookSuggestionAgent:
    def __init__(self):
        """Inicializa o agente de sugestões de livros."""
        logger.info("Inicializando BookSuggestionAgent")
        
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
        self.parser = PydanticOutputParser(pydantic_object=BookSuggestionList)
        
        # Configurar o template do prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um assistente especializado em criar sugestões de livros. 
            Com base na descrição fornecida, crie uma sugestão detalhada de livro.
            
            {format_instructions}
            
            Regras importantes:
            1. Use aspas duplas para strings
            2. Não use vírgula após o último item
            3. Não inclua texto adicional ou formatação markdown
            4. Não use blocos de código
            5. Retorne apenas o JSON válido"""),
            ("human", "Descrição: {description}")
        ])
        
        logger.info("BookSuggestionAgent inicializado com sucesso")
    
    def generate_suggestions(self, description: str) -> List[Dict[str, Any]]:
        """
        Gera sugestões de livros com base na descrição fornecida.
        
        Args:
            description (str): Descrição do livro desejado
            
        Returns:
            List[Dict[str, Any]]: Lista de sugestões de livros
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