from sqlalchemy import Column, String, Text
from src.database import Base
from src.utils.logger import logger

class Environment(Base):
    """Modelo para ambientes e cenários."""
    __tablename__ = 'environments'
    
    id = Column(String(36), primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)
    descricao = Column(Text, nullable=False)
    atmosfera = Column(Text, nullable=False)
    elementos_importantes = Column(Text, nullable=False)
    significado = Column(Text, nullable=False)
    
    def __init__(self, **kwargs):
        """Inicializa um novo ambiente."""
        logger.info("Inicializando novo ambiente")
        super().__init__(**kwargs)
    
    def to_dict(self):
        """Converte o ambiente para um dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo,
            'descricao': self.descricao,
            'atmosfera': self.atmosfera,
            'elementos_importantes': self.elementos_importantes,
            'significado': self.significado
        } 