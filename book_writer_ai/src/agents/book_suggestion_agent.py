import google.generativeai as genai
from src.config.settings import GOOGLE_API_KEY, GEMINI_MODEL, SUGGESTION_TEMPLATE
from src.utils.logger import logger
import json
import streamlit as st
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Configurar a API do Google
genai.configure(api_key=GOOGLE_API_KEY)

class BookSuggestionAgent:
    def __init__(self):
        """Inicializa o agente de sugestões de livros."""
        logger.info(f"Inicializando BookSuggestionAgent com modelo {GEMINI_MODEL}")
        self.llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7,
            max_output_tokens=2048,
        )
        self.prompt = PromptTemplate(
            input_variables=["description"],
            template=SUGGESTION_TEMPLATE
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        logger.info("BookSuggestionAgent inicializado com sucesso")

    def generate_suggestions(self, description: str) -> List[Dict[str, Any]]:
        """
        Gera sugestões de livros com base na descrição fornecida.
        
        Args:
            description (str): Descrição do livro para gerar sugestões
            
        Returns:
            List[Dict[str, Any]]: Lista de sugestões de livros
        """
        try:
            logger.info(f"Iniciando geração de sugestões para descrição: {description[:100]}...")
            
            # Configuração da geração
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            logger.debug(f"Configuração de geração: {generation_config}")
            
            # Gerar sugestões
            response = self.chain.run(description=description)
            logger.debug(f"Resposta bruta do modelo: {response}")
            
            if not response or not response.strip():
                logger.error("Resposta vazia do modelo")
                return []
            
            # Limpar a resposta para garantir que é um JSON válido
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            logger.debug(f"Resposta limpa: {response}")
            
            # Tentar decodificar o JSON
            try:
                suggestions = json.loads(response)
                logger.debug(f"JSON decodificado: {suggestions}")
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao decodificar JSON: {str(e)}")
                logger.error(f"Resposta recebida: {response}")
                return []
            
            # Validar campos obrigatórios
            required_fields = ["titulo", "volume", "autor", "genero", "idioma", "sinopse"]
            if not all(field in suggestions for field in required_fields):
                missing_fields = [field for field in required_fields if field not in suggestions]
                logger.error(f"Campos obrigatórios ausentes: {missing_fields}")
                return []
            
            logger.info("Sugestões geradas com sucesso")
            return [suggestions]
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões: {str(e)}", exc_info=True)
            return [] 