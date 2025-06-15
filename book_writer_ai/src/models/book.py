from sqlalchemy import Column, Integer, String, Text
from src.database import Base
from src.utils.logger import logger

class Book(Base):
    """Modelo para representar um livro no banco de dados."""
    
    __tablename__ = "books"
    
    id = Column(String(36), primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    volume = Column(String(50), nullable=False)
    autor = Column(String(255), nullable=False)
    genero = Column(String(100), nullable=False)
    idioma = Column(String(50), nullable=False)
    sinopse = Column(Text, nullable=True)
    estilo_narrativo = Column(String(50), nullable=True)
    publico_alvo = Column(String(50), nullable=True)
    
    def __init__(self, **kwargs):
        logger.debug(f"Inicializando Book com dados: {kwargs}")
        super().__init__(**kwargs)
    
    def to_dict(self):
        """Converte o objeto para um dicionário."""
        logger.debug(f"Convertendo Book para dicionário. ID: {self.id}")
        return {
            "id": self.id,
            "titulo": self.titulo,
            "volume": self.volume,
            "autor": self.autor,
            "genero": self.genero,
            "idioma": self.idioma,
            "sinopse": self.sinopse,
            "estilo_narrativo": self.estilo_narrativo,
            "publico_alvo": self.publico_alvo
        } 