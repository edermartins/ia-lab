from typing import Dict, Optional, Any
from database.models import Database
import sqlite3
import uuid

class EnvironmentManager:
    def __init__(self):
        self.db = Database()
    
    def save_environment(self, environment_data: Dict[str, Any]) -> str:
        """Salva um novo ambiente no banco de dados."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                env_id = str(uuid.uuid4())
                
                cursor.execute("""
                    INSERT INTO environments (
                        id, name, type, physical_description, atmosphere,
                        important_elements, significance, suggestions
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    env_id,
                    environment_data.get("name", ""),
                    environment_data.get("type", ""),
                    environment_data.get("physical_description", ""),
                    environment_data.get("atmosphere", ""),
                    environment_data.get("important_elements", ""),
                    environment_data.get("significance", ""),
                    environment_data.get("suggestions", "")
                ))
                
                # Se houver um story_id, cria um capítulo temporário para vincular o ambiente ao livro
                if environment_data.get("story_id"):
                    chapter_id = str(uuid.uuid4())
                    cursor.execute("""
                        INSERT INTO chapters (id, story_id, title, content)
                        VALUES (?, ?, ?, ?)
                    """, (chapter_id, environment_data["story_id"], "Capítulo Temporário", ""))
                    
                    cursor.execute("""
                        INSERT INTO chapter_environments (chapter_id, environment_id)
                        VALUES (?, ?)
                    """, (chapter_id, env_id))
                
                conn.commit()
                return env_id
        except Exception as e:
            print(f"Erro ao salvar ambiente: {e}")
            return None
    
    def get_environment(self, env_id: str) -> Optional[Dict]:
        """Recupera um ambiente do banco de dados."""
        return self.db.get_environment(env_id)
    
    def get_all_environments(self) -> Dict[str, Dict]:
        """Recupera todos os ambientes do banco de dados."""
        return self.db.get_all_environments()

    def _ensure_data_directory(self):
        """Garante que o diretório de dados existe."""
        pass
    
    def _load_environments(self):
        """Carrega os ambientes do arquivo JSON."""
        pass
    
    def _save_environments(self):
        """Salva os ambientes no arquivo JSON."""
        pass
    
    def delete_environment(self, env_id: str) -> bool:
        """Deleta um ambiente do banco de dados."""
        return self.db.delete_environment(env_id)
    
    def update_environment(self, environment_id: str, environment_data: Dict[str, Any]) -> bool:
        """Atualiza um ambiente existente."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE environments 
                    SET name = ?, type = ?, physical_description = ?, 
                        atmosphere = ?, important_elements = ?, significance = ?, 
                        suggestions = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (
                    environment_data["name"],
                    environment_data.get("type", ""),
                    environment_data.get("physical_description", ""),
                    environment_data.get("atmosphere", ""),
                    environment_data.get("important_elements", ""),
                    environment_data.get("significance", ""),
                    environment_data.get("suggestions", ""),
                    environment_id
                ))
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar ambiente: {e}")
            return False

    def get_book_environments(self, story_id: str) -> Dict[str, Dict]:
        """Retorna todos os ambientes associados a um livro específico."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT e.id, e.name, e.type, e.physical_description, e.atmosphere, 
                           e.important_elements, e.significance, e.suggestions
                    FROM environments e
                    JOIN chapter_environments ce ON e.id = ce.environment_id
                    JOIN chapters c ON ce.chapter_id = c.id
                    WHERE c.story_id = ?
                    GROUP BY e.id
                """, (story_id,))
                
                environments = {}
                for row in cursor.fetchall():
                    env_id = row[0]
                    environments[env_id] = {
                        "name": row[1],
                        "type": row[2],
                        "physical_description": row[3],
                        "atmosphere": row[4],
                        "important_elements": row[5],
                        "significance": row[6],
                        "suggestions": row[7]
                    }
                return environments
        except Exception as e:
            print(f"Erro ao buscar ambientes do livro: {e}")
            return {} 