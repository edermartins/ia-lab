from sqlalchemy.orm import Session
from src.models.environment import Environment
from src.database import get_db
from src.agents.environment_suggestion_agent import EnvironmentSuggestionAgent
from src.utils.logger import logger
import uuid

class EnvironmentService:
    """Serviço para gerenciar ambientes e cenários."""
    
    def __init__(self):
        """Inicializa o serviço de ambientes."""
        logger.info("Inicializando EnvironmentService")
        self.suggestion_agent = EnvironmentSuggestionAgent()
    
    def create_environment(self, environment_data: dict) -> dict:
        """
        Cria um novo ambiente.
        
        Args:
            environment_data (dict): Dados do ambiente
            
        Returns:
            dict: Ambiente criado
        """
        logger.info(f"Criando novo ambiente: {environment_data.get('nome', 'Sem nome')}")
        try:
            with get_db() as db:
                environment = Environment(
                    id=str(uuid.uuid4()),
                    **environment_data
                )
                db.add(environment)
                db.commit()
                db.refresh(environment)
                logger.info(f"Ambiente criado com sucesso: {environment.id}")
                return environment.to_dict()
        except Exception as e:
            logger.error(f"Erro ao criar ambiente: {str(e)}", exc_info=True)
            raise
    
    def get_all_environments(self) -> list:
        """
        Retorna todos os ambientes.
        
        Returns:
            list: Lista de ambientes
        """
        logger.info("Buscando todos os ambientes")
        try:
            with get_db() as db:
                environments = db.query(Environment).all()
                logger.info(f"Encontrados {len(environments)} ambientes")
                return [env.to_dict() for env in environments]
        except Exception as e:
            logger.error(f"Erro ao buscar ambientes: {str(e)}", exc_info=True)
            raise
    
    def get_environment_by_id(self, environment_id: str) -> dict:
        """
        Busca um ambiente pelo ID.
        
        Args:
            environment_id (str): ID do ambiente
            
        Returns:
            dict: Ambiente encontrado
        """
        logger.info(f"Buscando ambiente com ID: {environment_id}")
        try:
            with get_db() as db:
                environment = db.query(Environment).filter(Environment.id == environment_id).first()
                if environment:
                    logger.info(f"Ambiente encontrado: {environment.id}")
                    return environment.to_dict()
                logger.warning(f"Ambiente não encontrado: {environment_id}")
                return None
        except Exception as e:
            logger.error(f"Erro ao buscar ambiente: {str(e)}", exc_info=True)
            raise
    
    def update_environment(self, environment_id: str, environment_data: dict) -> dict:
        """
        Atualiza um ambiente.
        
        Args:
            environment_id (str): ID do ambiente
            environment_data (dict): Novos dados do ambiente
            
        Returns:
            dict: Ambiente atualizado
        """
        logger.info(f"Atualizando ambiente: {environment_id}")
        try:
            with get_db() as db:
                environment = db.query(Environment).filter(Environment.id == environment_id).first()
                if environment:
                    for key, value in environment_data.items():
                        setattr(environment, key, value)
                    db.commit()
                    db.refresh(environment)
                    logger.info(f"Ambiente atualizado com sucesso: {environment.id}")
                    return environment.to_dict()
                logger.warning(f"Ambiente não encontrado para atualização: {environment_id}")
                return None
        except Exception as e:
            logger.error(f"Erro ao atualizar ambiente: {str(e)}", exc_info=True)
            raise
    
    def delete_environment(self, environment_id: str) -> bool:
        """
        Remove um ambiente.
        
        Args:
            environment_id (str): ID do ambiente
            
        Returns:
            bool: True se removido com sucesso
        """
        logger.info(f"Removendo ambiente: {environment_id}")
        try:
            with get_db() as db:
                environment = db.query(Environment).filter(Environment.id == environment_id).first()
                if environment:
                    db.delete(environment)
                    db.commit()
                    logger.info(f"Ambiente removido com sucesso: {environment_id}")
                    return True
                logger.warning(f"Ambiente não encontrado para remoção: {environment_id}")
                return False
        except Exception as e:
            logger.error(f"Erro ao remover ambiente: {str(e)}", exc_info=True)
            raise
    
    def generate_suggestions(self, description: str) -> list:
        """
        Gera sugestões de ambientes usando IA.
        
        Args:
            description (str): Descrição do ambiente desejado
            
        Returns:
            list: Lista de sugestões de ambientes
        """
        logger.info("Gerando sugestões de ambientes")
        try:
            suggestions = self.suggestion_agent.generate_suggestions(description)
            logger.info(f"Geradas {len(suggestions)} sugestões de ambientes")
            return suggestions
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões de ambientes: {str(e)}", exc_info=True)
            raise 