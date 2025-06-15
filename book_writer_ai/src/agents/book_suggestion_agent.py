import google.generativeai as genai
import json
from src.config.settings import GOOGLE_API_KEY, SUGGESTION_TEMPLATE
from src.utils.logger import logger

class BookSuggestionAgent:
    def __init__(self):
        logger.info("Inicializando BookSuggestionAgent")
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def generate_suggestions(self, description: str) -> list:
        """Gera sugestões de livros baseadas na descrição fornecida."""
        logger.info(f"Gerando sugestões para descrição: {description[:100]}...")
        
        try:
            # Gerar o prompt
            prompt = SUGGESTION_TEMPLATE.format(description=description)
            
            # Configurar parâmetros de geração
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            # Gerar conteúdo
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Log da resposta bruta
            logger.debug(f"Resposta bruta do modelo: {response.text}")
            
            # Limpar a resposta (remover possíveis formatações markdown)
            cleaned_response = response.text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            logger.debug(f"Resposta limpa: {cleaned_response}")
            
            # Tentar decodificar o JSON
            try:
                suggestions = json.loads(cleaned_response)
                logger.info(f"Sugestões decodificadas: {suggestions}")
                
                # Validar campos obrigatórios
                required_fields = [
                    'titulo', 'volume', 'autor', 'genero', 'idioma', 'sinopse',
                    'estilo_narrativo', 'publico_alvo'
                ]
                valid_suggestions = []
                
                for suggestion in suggestions:
                    missing_fields = [field for field in required_fields if field not in suggestion]
                    if missing_fields:
                        logger.warning(f"Sugestão inválida - campos faltando: {missing_fields}")
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