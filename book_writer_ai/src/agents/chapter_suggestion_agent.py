import os
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from src.utils.logger import logger

class ChapterSuggestion(BaseModel):
    titulo: str = Field(description="Título do capítulo")
    ordem: int = Field(description="Ordem do capítulo")
    texto: str = Field(description="Texto do capítulo")

class ChapterSuggestionAgent:
    def __init__(self):
        logger.info("Inicializando ChapterSuggestionAgent")
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0.7,
            top_p=0.8,
            top_k=40,
            max_output_tokens=2048,
            convert_system_message_to_human=True
        )
        self.parser = PydanticOutputParser(pydantic_object=ChapterSuggestion)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", '''Você é um escritor com longa experiência em criar livros com temas variádos.\nCom base na sugestão do autor, dos personagens e ambientes selecionados, gere um capítulo completo com tamanho entre 1000 e 5000 palavras.\n\n{format_instructions}\n\nRegras importantes:\n1. Use aspas duplas para strings\n2. Não use vírgula após o último item\n3. Não inclua texto adicional ou formatação markdown\n4. Não use blocos de código\n5. Retorne apenas o JSON válido'''),
            ("human", "Sugestão: {sugestao}\nPersonagens: {personagens}\nAmbientes: {ambientes}")
        ])
        logger.info("ChapterSuggestionAgent inicializado com sucesso")

    def generate_suggestion(self, sugestao: str, personagens: List[Dict[str, Any]], ambientes: List[Dict[str, Any]]) -> Dict[str, Any]:
        logger.info("Gerando sugestão de capítulo via LLM...")
        try:
            personagens_str = ", ".join([p['nome'] for p in personagens])
            ambientes_str = ", ".join([a['nome'] for a in ambientes])
            prompt = self.prompt.format_messages(
                sugestao=sugestao,
                personagens=personagens_str,
                ambientes=ambientes_str,
                format_instructions=self.parser.get_format_instructions()
            )
            response = self.model.invoke(prompt)
            logger.info(f"Resposta bruta recebida: {response.content[:200]}...")
            result = self.parser.parse(response.content)
            return result.dict()
        except Exception as e:
            logger.error(f"Erro ao gerar sugestão de capítulo: {str(e)}", exc_info=True)
            return {} 