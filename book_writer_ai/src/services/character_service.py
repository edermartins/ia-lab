import logging
from sqlalchemy.orm import Session
from src.models.character import Character
from src.agents.character_suggestion_agent import CharacterSuggestionAgent
from src.database import get_db
from src.utils.logger import logger
import uuid

class CharacterService:
    def __init__(self):
        logger.info("Inicializando CharacterService")
        self.suggestion_agent = CharacterSuggestionAgent()
    
    def create_character(self, character_data: dict) -> dict:
        """
        Cria um novo personagem no banco de dados.
        
        Args:
            character_data (dict): Dados do personagem a ser criado
            
        Returns:
            dict: Dados do personagem criado
        """
        logger.info(f"Tentando criar novo personagem com dados: {character_data}")
        try:
            with get_db() as db:
                logger.debug("Criando nova instância de Character")
                new_character = Character(
                    id=str(uuid.uuid4()),
                    nome=character_data['nome'],
                    idade=character_data['idade'],
                    papel=character_data['papel'],
                    caracteristicas_fisicas=character_data['caracteristicas_fisicas'],
                    personalidade=character_data['personalidade'],
                    historico=character_data['historico']
                )
                
                logger.debug("Adicionando personagem à sessão do banco de dados")
                db.add(new_character)
                
                logger.debug("Realizando commit das alterações")
                db.commit()
                
                logger.debug("Atualizando a instância com os dados do banco")
                db.refresh(new_character)
                
                logger.info(f"Personagem criado com sucesso. ID: {new_character.id}")
                return new_character.to_dict()
        except Exception as e:
            logger.error(f"Erro ao criar personagem: {str(e)}", exc_info=True)
            raise
    
    def get_all_characters(self) -> list:
        """
        Retorna todos os personagens cadastrados.
        
        Returns:
            list: Lista de personagens
        """
        logger.info("Buscando todos os personagens")
        try:
            with get_db() as db:
                characters = db.query(Character).all()
                logger.info(f"Encontrados {len(characters)} personagens")
                return [character.to_dict() for character in characters]
        except Exception as e:
            logger.error(f"Erro ao buscar personagens: {str(e)}", exc_info=True)
            raise
    
    def get_character_by_id(self, character_id: str) -> dict:
        """
        Busca um personagem pelo ID.
        
        Args:
            character_id (str): ID do personagem
            
        Returns:
            dict: Dados do personagem
        """
        logger.info(f"Buscando personagem com ID: {character_id}")
        try:
            with get_db() as db:
                character = db.query(Character).filter(Character.id == character_id).first()
                if character:
                    logger.info(f"Personagem encontrado: {character.to_dict()}")
                    return character.to_dict()
                logger.warning(f"Personagem não encontrado: {character_id}")
                return None
        except Exception as e:
            logger.error(f"Erro ao buscar personagem: {str(e)}", exc_info=True)
            raise
    
    def update_character(self, character_id: str, character_data: dict) -> dict:
        """
        Atualiza um personagem existente.
        
        Args:
            character_id (str): ID do personagem
            character_data (dict): Novos dados do personagem
            
        Returns:
            dict: Dados do personagem atualizado
        """
        logger.info(f"Atualizando personagem {character_id} com dados: {character_data}")
        try:
            with get_db() as db:
                character = db.query(Character).filter(Character.id == character_id).first()
                if not character:
                    logger.warning(f"Personagem não encontrado: {character_id}")
                    return None
                
                for key, value in character_data.items():
                    setattr(character, key, value)
                
                db.commit()
                db.refresh(character)
                logger.info(f"Personagem atualizado com sucesso: {character.to_dict()}")
                return character.to_dict()
        except Exception as e:
            logger.error(f"Erro ao atualizar personagem: {str(e)}", exc_info=True)
            raise
    
    def delete_character(self, character_id: str) -> bool:
        """
        Remove um personagem.
        
        Args:
            character_id (str): ID do personagem
            
        Returns:
            bool: True se o personagem foi removido, False caso contrário
        """
        logger.info(f"Removendo personagem: {character_id}")
        try:
            with get_db() as db:
                character = db.query(Character).filter(Character.id == character_id).first()
                if not character:
                    logger.warning(f"Personagem não encontrado: {character_id}")
                    return False
                
                db.delete(character)
                db.commit()
                logger.info(f"Personagem removido com sucesso: {character_id}")
                return True
        except Exception as e:
            logger.error(f"Erro ao remover personagem: {str(e)}", exc_info=True)
            raise
    
    def generate_suggestions(self, description: str) -> list:
        """
        Gera sugestões de personagens baseadas na descrição fornecida.
        
        Args:
            description (str): Descrição do personagem desejado
            
        Returns:
            list: Lista de sugestões de personagens
        """
        logger.info(f"Gerando sugestões para descrição: {description[:100]}...")
        try:
            suggestions = self.suggestion_agent.generate_suggestions(description)
            if suggestions:
                logger.info(f"Geradas {len(suggestions)} sugestões")
                return suggestions
            logger.warning("Nenhuma sugestão gerada")
            return []
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões: {str(e)}", exc_info=True)
            raise 