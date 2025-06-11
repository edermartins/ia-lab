from typing import Dict, Optional, Any
from database.models import Database
import sqlite3

class CharacterManager:
    def __init__(self):
        self.db = Database()
    
    def save_character(self, character_data: Dict) -> str:
        """Salva um personagem no banco de dados."""
        return self.db.save_character(character_data)
    
    def get_character(self, char_id: str) -> Optional[Dict]:
        """Recupera um personagem do banco de dados."""
        return self.db.get_character(char_id)
    
    def get_all_characters(self) -> Dict[str, Dict]:
        """Recupera todos os personagens do banco de dados."""
        return self.db.get_all_characters()
    
    def delete_character(self, char_id: str) -> bool:
        """Deleta um personagem do banco de dados."""
        return self.db.delete_character(char_id)
    
    def update_character(self, character_id: str, character_data: Dict[str, Any]) -> bool:
        """Atualiza um personagem existente."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE characters 
                    SET name = ?, age = ?, role = ?, physical_traits = ?, 
                        personality = ?, background = ?, suggestions = ?, 
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (
                    character_data["name"],
                    character_data.get("age", 0),
                    character_data.get("role", "Protagonista"),
                    character_data.get("physical_traits", ""),
                    character_data.get("personality", ""),
                    character_data.get("background", ""),
                    character_data.get("suggestions", ""),
                    character_id
                ))
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar personagem: {e}")
            return False 