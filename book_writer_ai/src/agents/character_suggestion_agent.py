import os
import json
import google.generativeai as genai
from src.config.settings import CHARACTER_SUGGESTION_TEMPLATE
from src.utils.logger import logger

class CharacterSuggestionAgent:
    def __init__(self):
        """Inicializa o agente de sugestões de personagens."""
        logger.info("Inicializando CharacterSuggestionAgent")
        
        # Configurar a API do Google
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")
        
        genai.configure(api_key=api_key)
        
        # Inicializar o modelo
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        logger.info("CharacterSuggestionAgent inicializado com sucesso")
    
    def generate_suggestions(self, description: str) -> list:
        """
        Gera sugestões de personagens com base na descrição fornecida.
        
        Args:
            description (str): Descrição do personagem desejado
            
        Returns:
            list: Lista de sugestões de personagens
        """
        logger.info(f"Gerando sugestões para descrição: {description[:100]}...")
        
        try:
            # Gerar o prompt
            prompt = CHARACTER_SUGGESTION_TEMPLATE.format(description=description)
            logger.info(f"Iniciando geração de sugestões para descrição: {description[:100]}...")
            
            # Configurar a geração
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            # Gerar a resposta
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Log da resposta bruta
            logger.info(f"Resposta bruta recebida: {response.text[:200]}...")
            
            # Limpar a resposta (remover possíveis markdown)
            cleaned_response = response.text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            # Log da resposta limpa
            logger.info(f"Resposta limpa: {cleaned_response[:200]}...")
            
            # Tentar decodificar o JSON
            try:
                suggestions = json.loads(cleaned_response)
                logger.info(f"Sugestões decodificadas: {json.dumps(suggestions, indent=2)}")
                
                # Converter para lista se for um dicionário
                if isinstance(suggestions, dict):
                    suggestions = [suggestions]
                elif not isinstance(suggestions, list):
                    logger.error(f"Formato inválido: esperava uma lista ou dicionário, recebeu {type(suggestions)}")
                    return []
                
                # Verificar campos obrigatórios
                required_fields = ['nome', 'idade', 'papel', 'caracteristicas_fisicas', 'personalidade', 'historico']
                valid_suggestions = []
                
                for suggestion in suggestions:
                    missing_fields = [field for field in required_fields if field not in suggestion]
                    if missing_fields:
                        logger.warning(f"Sugestão ignorada - campos faltando: {missing_fields}")
                        continue
                    valid_suggestions.append(suggestion)
                
                if valid_suggestions:
                    logger.info(f"Retornando {len(valid_suggestions)} sugestões válidas")
                    return valid_suggestions
                else:
                    logger.warning("Nenhuma sugestão válida encontrada")
                    return []
                
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao decodificar JSON: {str(e)}")
                logger.error(f"Conteúdo que causou o erro: {cleaned_response}")
                return []
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões: {str(e)}", exc_info=True)
            return [] 