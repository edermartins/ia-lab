import uuid
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.chapter import Chapter
from src.utils.logger import logger

class ChapterService:
    def __init__(self):
        """Inicializa o serviço de capítulos."""
        logger.info("Inicializando ChapterService")

    def create_chapter(self, chapter_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo capítulo."""
        logger.info(f"Criando novo capítulo: {chapter_data}")
        try:
            with get_db() as db:
                chapter = Chapter(
                    id=str(uuid.uuid4()),
                    **chapter_data
                )
                db.add(chapter)
                db.commit()
                db.refresh(chapter)
                logger.info(f"Capítulo criado com sucesso: {chapter.id}")
                return chapter.to_dict()
        except Exception as e:
            logger.error(f"Erro ao criar capítulo: {str(e)}", exc_info=True)
            raise

    def get_chapter_by_id(self, chapter_id: str) -> Dict[str, Any]:
        """Obtém um capítulo pelo ID."""
        logger.info(f"Buscando capítulo: {chapter_id}")
        try:
            with get_db() as db:
                chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
                if chapter:
                    logger.info(f"Capítulo encontrado: {chapter_id}")
                    return chapter.to_dict()
                logger.warning(f"Capítulo não encontrado: {chapter_id}")
                return None
        except Exception as e:
            logger.error(f"Erro ao buscar capítulo: {str(e)}", exc_info=True)
            raise

    def get_chapters_by_book_id(self, book_id: str) -> List[Dict[str, Any]]:
        """Obtém todos os capítulos de um livro."""
        logger.info(f"Buscando capítulos do livro: {book_id}")
        try:
            with get_db() as db:
                chapters = db.query(Chapter).filter(Chapter.book_id == book_id).order_by(Chapter.ordem).all()
                logger.info(f"Encontrados {len(chapters)} capítulos para o livro {book_id}")
                return [chapter.to_dict() for chapter in chapters]
        except Exception as e:
            logger.error(f"Erro ao buscar capítulos do livro: {str(e)}", exc_info=True)
            raise

    def update_chapter(self, chapter_id: str, chapter_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um capítulo existente."""
        logger.info(f"Atualizando capítulo {chapter_id}: {chapter_data}")
        try:
            with get_db() as db:
                chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
                if not chapter:
                    logger.warning(f"Capítulo não encontrado: {chapter_id}")
                    return None

                for key, value in chapter_data.items():
                    setattr(chapter, key, value)

                db.commit()
                db.refresh(chapter)
                logger.info(f"Capítulo atualizado com sucesso: {chapter_id}")
                return chapter.to_dict()
        except Exception as e:
            logger.error(f"Erro ao atualizar capítulo: {str(e)}", exc_info=True)
            raise

    def delete_chapter(self, chapter_id: str) -> bool:
        """Remove um capítulo."""
        logger.info(f"Removendo capítulo: {chapter_id}")
        try:
            with get_db() as db:
                chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
                if not chapter:
                    logger.warning(f"Capítulo não encontrado: {chapter_id}")
                    return False

                db.delete(chapter)
                db.commit()
                logger.info(f"Capítulo removido com sucesso: {chapter_id}")
                return True
        except Exception as e:
            logger.error(f"Erro ao remover capítulo: {str(e)}", exc_info=True)
            raise 