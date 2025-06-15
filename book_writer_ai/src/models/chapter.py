from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from src.utils.logger import logger

class Chapter(Base):
    """Modelo para representar um capítulo no banco de dados."""
    
    __tablename__ = "chapters"

    id = Column(String(36), primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    ordem = Column(Integer, nullable=False)
    texto = Column(Text, nullable=False)
    descricao_autor = Column(Text, nullable=True)
    book_id = Column(String(36), ForeignKey("books.id"), nullable=False)

    # Relacionamento com Book
    book = relationship("Book", back_populates="chapters")

    def __init__(self, **kwargs):
        logger.debug(f"Inicializando Chapter com dados: {kwargs}")
        super().__init__(**kwargs)

    def to_dict(self):
        """Converte o objeto para um dicionário."""
        logger.debug(f"Convertendo Chapter para dicionário. ID: {self.id}")
        return {
            "id": self.id,
            "titulo": self.titulo,
            "ordem": self.ordem,
            "texto": self.texto,
            "descricao_autor": self.descricao_autor,
            "book_id": self.book_id
        } 