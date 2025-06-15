import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from src.models.book import Book
from src.database import get_db
from src.agents.book_suggestion_agent import BookSuggestionAgent
from src.config.settings import SUGGESTION_TEMPLATE
from src.utils.logger import logger

class BookService:
    def __init__(self):
        """Inicializa o serviço de livros."""
        logger.info("Inicializando BookService")
        self.suggestion_agent = BookSuggestionAgent()
    
    def create_book(self, book_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo livro no banco de dados.
        
        Args:
            book_data (Dict[str, Any]): Dados do livro a ser criado
            
        Returns:
            Dict[str, Any]: Dados do livro criado
        """
        logger.info(f"Tentando criar novo livro com dados: {book_data}")
        try:
            with get_db() as db:
                logger.debug("Criando nova instância de Book")
                new_book = Book(
                    titulo=book_data['titulo'],
                    volume=book_data['volume'],
                    autor=book_data['autor'],
                    genero=book_data['genero'],
                    idioma=book_data['idioma'],
                    sinopse=book_data.get('sinopse', '')
                )
                
                logger.debug("Adicionando livro à sessão do banco de dados")
                db.add(new_book)
                
                logger.debug("Realizando commit das alterações")
                db.commit()
                
                logger.debug("Atualizando a instância com os dados do banco")
                db.refresh(new_book)
                
                logger.info(f"Livro criado com sucesso. ID: {new_book.id}")
                return new_book.to_dict()
        except Exception as e:
            logger.error(f"Erro ao criar livro: {str(e)}", exc_info=True)
            raise
    
    def get_all_books(self) -> List[Dict[str, Any]]:
        """
        Retorna todos os livros cadastrados.
        
        Returns:
            List[Dict[str, Any]]: Lista de livros
        """
        logger.info("Buscando todos os livros")
        try:
            with get_db() as db:
                books = db.query(Book).all()
                logger.info(f"Encontrados {len(books)} livros")
                return [book.to_dict() for book in books]
        except Exception as e:
            logger.error(f"Erro ao buscar livros: {str(e)}", exc_info=True)
            raise
    
    def get_book_by_id(self, book_id: int) -> Dict[str, Any]:
        """
        Busca um livro pelo ID.
        
        Args:
            book_id (int): ID do livro
            
        Returns:
            Dict[str, Any]: Dados do livro
        """
        logger.info(f"Buscando livro com ID: {book_id}")
        try:
            with get_db() as db:
                book = db.query(Book).filter(Book.id == book_id).first()
                if book:
                    logger.info(f"Livro encontrado: {book.to_dict()}")
                    return book.to_dict()
                logger.warning(f"Livro não encontrado: {book_id}")
                return None
        except Exception as e:
            logger.error(f"Erro ao buscar livro: {str(e)}", exc_info=True)
            raise
    
    def update_book(self, book_id: int, book_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza um livro existente.
        
        Args:
            book_id (int): ID do livro
            book_data (Dict[str, Any]): Novos dados do livro
            
        Returns:
            Dict[str, Any]: Dados do livro atualizado
        """
        logger.info(f"Atualizando livro {book_id} com dados: {book_data}")
        try:
            with get_db() as db:
                book = db.query(Book).filter(Book.id == book_id).first()
                if not book:
                    logger.warning(f"Livro não encontrado: {book_id}")
                    return None
                
                for key, value in book_data.items():
                    setattr(book, key, value)
                
                db.commit()
                db.refresh(book)
                logger.info(f"Livro atualizado com sucesso: {book.to_dict()}")
                return book.to_dict()
        except Exception as e:
            logger.error(f"Erro ao atualizar livro: {str(e)}", exc_info=True)
            raise
    
    def delete_book(self, book_id: int) -> bool:
        """
        Remove um livro.
        
        Args:
            book_id (int): ID do livro
            
        Returns:
            bool: True se o livro foi removido, False caso contrário
        """
        logger.info(f"Removendo livro: {book_id}")
        try:
            with get_db() as db:
                book = db.query(Book).filter(Book.id == book_id).first()
                if not book:
                    logger.warning(f"Livro não encontrado: {book_id}")
                    return False
                
                db.delete(book)
                db.commit()
                logger.info(f"Livro removido com sucesso: {book_id}")
                return True
        except Exception as e:
            logger.error(f"Erro ao remover livro: {str(e)}", exc_info=True)
            raise
    
    def generate_suggestions(self, description: str) -> List[Dict[str, Any]]:
        """
        Gera sugestões de livros baseadas na descrição fornecida.
        
        Args:
            description (str): Descrição do livro desejado
            
        Returns:
            List[Dict[str, Any]]: Lista de sugestões de livros
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