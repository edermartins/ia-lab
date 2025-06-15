from sqlalchemy import Column, String, Text, Integer
from src.database import Base
from src.utils.logger import logger

class Character(Base):
    """Modelo para representar um personagem no banco de dados."""
    
    __tablename__ = "characters"
    
    id = Column(String(36), primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    idade = Column(Integer, nullable=False)
    papel = Column(String(255), nullable=False)
    caracteristicas_fisicas = Column(Text, nullable=False)
    personalidade = Column(Text, nullable=False)
    historico = Column(Text, nullable=False)
    
    def __init__(self, **kwargs):
        logger.debug(f"Inicializando Character com dados: {kwargs}")
        super().__init__(**kwargs)
    
    def to_dict(self):
        """Converte o objeto para um dicionário."""
        logger.debug(f"Convertendo Character para dicionário. ID: {self.id}")
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "papel": self.papel,
            "caracteristicas_fisicas": self.caracteristicas_fisicas,
            "personalidade": self.personalidade,
            "historico": self.historico
        } 