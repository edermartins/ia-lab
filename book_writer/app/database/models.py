import sqlite3
from typing import Dict, List, Optional, Any
import json
import uuid

class Database:
    def __init__(self, db_path: str = "book_writer.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Inicializa o banco de dados com as tabelas necessárias."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de Histórias
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stories (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    genre TEXT,
                    target_audience TEXT,
                    main_theme TEXT,
                    narrative_style TEXT,
                    setting TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de Personagens
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                    id TEXT PRIMARY KEY,
                    story_id TEXT,
                    name TEXT NOT NULL,
                    role TEXT,
                    description TEXT,
                    background TEXT,
                    goals TEXT,
                    conflicts TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES stories (id)
                )
            """)
            
            # Tabela de Ambientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS environments (
                    id TEXT PRIMARY KEY,
                    story_id TEXT,
                    name TEXT NOT NULL,
                    type TEXT,
                    physical_description TEXT,
                    atmosphere TEXT,
                    important_elements TEXT,
                    significance TEXT,
                    suggestions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES stories (id)
                )
            """)
            
            # Tabela de Capítulos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chapters (
                    id TEXT PRIMARY KEY,
                    story_id TEXT,
                    title TEXT NOT NULL,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES stories (id)
                )
            """)
            
            # Tabela de Eventos da Linha do Tempo
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS timeline_events (
                    id TEXT PRIMARY KEY,
                    story_id TEXT,
                    title TEXT NOT NULL,
                    description TEXT,
                    date TEXT,
                    importance TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES stories (id)
                )
            """)
            
            # Tabela de Relacionamento Capítulo-Personagem
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chapter_characters (
                    chapter_id TEXT,
                    character_id TEXT,
                    PRIMARY KEY (chapter_id, character_id),
                    FOREIGN KEY (chapter_id) REFERENCES chapters (id),
                    FOREIGN KEY (character_id) REFERENCES characters (id)
                )
            """)
            
            # Tabela de Relacionamento Capítulo-Ambiente
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chapter_environments (
                    chapter_id TEXT,
                    environment_id TEXT,
                    PRIMARY KEY (chapter_id, environment_id),
                    FOREIGN KEY (chapter_id) REFERENCES chapters (id),
                    FOREIGN KEY (environment_id) REFERENCES environments (id)
                )
            """)
            
            conn.commit()
    
    def save_character(self, character_data: Dict[str, Any]) -> str:
        """Salva um novo personagem no banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                char_id = str(uuid.uuid4())
                
                cursor.execute("""
                    INSERT INTO characters (
                        id, name, role, description, background, goals, conflicts
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    char_id,
                    character_data.get("name", ""),
                    character_data.get("role", ""),
                    character_data.get("description", ""),
                    character_data.get("background", ""),
                    character_data.get("goals", ""),
                    character_data.get("conflicts", "")
                ))
                
                conn.commit()
                return char_id
        except Exception as e:
            print(f"Erro ao salvar personagem: {e}")
            return None
    
    def get_character(self, char_id: str) -> Optional[Dict]:
        """Retorna um personagem específico do banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, role, description, background, goals, conflicts
                    FROM characters
                    WHERE id = ?
                """, (char_id,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                return {
                    "id": row[0],
                    "name": row[1],
                    "role": row[2],
                    "description": row[3],
                    "background": row[4],
                    "goals": row[5],
                    "conflicts": row[6]
                }
        except Exception as e:
            print(f"Erro ao buscar personagem: {e}")
            return None
    
    def get_all_characters(self) -> Dict[str, Dict]:
        """Recupera todos os personagens do banco de dados."""
        characters = {}
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters")
            for row in cursor.fetchall():
                characters[row[0]] = {
                    "id": row[0],
                    "name": row[1],
                    "age": row[2],
                    "role": row[3],
                    "physical_traits": row[4],
                    "personality": row[5],
                    "background": row[6],
                    "suggestions": row[7]
                }
        return characters
    
    def save_environment(self, environment_data: Dict[str, Any]) -> str:
        """Salva um novo ambiente no banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                env_id = str(uuid.uuid4())
                
                cursor.execute("""
                    INSERT INTO environments (
                        id, story_id, name, type, physical_description,
                        atmosphere, important_elements, significance, suggestions
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    env_id,
                    environment_data.get("story_id"),
                    environment_data.get("name"),
                    environment_data.get("type"),
                    environment_data.get("physical_description"),
                    environment_data.get("atmosphere"),
                    environment_data.get("important_elements"),
                    environment_data.get("significance"),
                    environment_data.get("suggestions")
                ))
                
                conn.commit()
                return env_id
        except Exception as e:
            print(f"Erro ao salvar ambiente: {e}")
            return None
    
    def get_environment(self, env_id: str) -> Optional[Dict]:
        """Recupera um ambiente do banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM environments WHERE id = ?", (env_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "type": row[2],
                    "physical_description": row[3],
                    "atmosphere": row[4],
                    "important_elements": row[5],
                    "significance": row[6],
                    "suggestions": row[7]
                }
        return None
    
    def get_all_environments(self) -> Dict[str, Dict]:
        """Recupera todos os ambientes do banco de dados."""
        environments = {}
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM environments")
            for row in cursor.fetchall():
                environments[row[0]] = {
                    "id": row[0],
                    "name": row[1],
                    "type": row[2],
                    "physical_description": row[3],
                    "atmosphere": row[4],
                    "important_elements": row[5],
                    "significance": row[6],
                    "suggestions": row[7]
                }
        return environments
    
    def save_story(self, story_data: Dict[str, Any]) -> str:
        """Salva uma nova história no banco de dados."""
        try:
            story_id = str(uuid.uuid4())
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO stories (
                        id, title, description, genre, target_audience,
                        main_theme, narrative_style, setting
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    story_id,
                    story_data.get('title'),
                    story_data.get('description'),
                    story_data.get('genre'),
                    story_data.get('target_audience'),
                    story_data.get('main_theme'),
                    story_data.get('narrative_style'),
                    story_data.get('setting')
                ))
                conn.commit()
            return story_id
        except Exception as e:
            print(f"Erro ao salvar história: {e}")
            return None
    
    def get_story(self, story_id: str) -> Optional[Dict]:
        """Retorna uma história específica do banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, title, description, genre, target_audience,
                           main_theme, narrative_style, setting,
                           created_at, updated_at
                    FROM stories
                    WHERE id = ?
                """, (story_id,))
                row = cursor.fetchone()
                if not row:
                    return None
                return {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'genre': row[3],
                    'target_audience': row[4],
                    'main_theme': row[5],
                    'narrative_style': row[6],
                    'setting': row[7],
                    'created_at': row[8],
                    'updated_at': row[9]
                }
        except Exception as e:
            print(f"Erro ao buscar história: {e}")
            return None
    
    def save_chapter(self, chapter_data: Dict[str, Any]) -> str:
        """Salva um novo capítulo no banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                chapter_id = str(uuid.uuid4())
                
                cursor.execute("""
                    INSERT INTO chapters (
                        id, story_id, title, content
                    ) VALUES (?, ?, ?, ?)
                """, (
                    chapter_id,
                    chapter_data.get("story_id"),
                    chapter_data.get("title"),
                    chapter_data.get("content")
                ))
                
                # Salva os personagens do capítulo
                for char_id in chapter_data.get("characters", []):
                    cursor.execute("""
                        INSERT INTO chapter_characters (
                            chapter_id, character_id
                        ) VALUES (?, ?)
                    """, (chapter_id, char_id))
                
                # Salva os ambientes do capítulo
                for env_id in chapter_data.get("environments", []):
                    cursor.execute("""
                        INSERT INTO chapter_environments (
                            chapter_id, environment_id
                        ) VALUES (?, ?)
                    """, (chapter_id, env_id))
                
                conn.commit()
                return chapter_id
        except Exception as e:
            print(f"Erro ao salvar capítulo: {e}")
            return None
    
    def get_chapter(self, chapter_id: str) -> Optional[Dict]:
        """Retorna um capítulo específico do banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, story_id, title, content
                    FROM chapters
                    WHERE id = ?
                """, (chapter_id,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                chapter = {
                    "id": row[0],
                    "story_id": row[1],
                    "title": row[2],
                    "content": row[3],
                    "characters": {},
                    "environments": {}
                }
                
                # Busca os personagens do capítulo
                cursor.execute("""
                    SELECT c.id, c.name, c.role, c.description, c.background, c.goals, c.conflicts
                    FROM characters c
                    JOIN chapter_characters cc ON c.id = cc.character_id
                    WHERE cc.chapter_id = ?
                """, (chapter_id,))
                
                for char_row in cursor.fetchall():
                    char_id = char_row[0]
                    chapter["characters"][char_id] = {
                        "name": char_row[1],
                        "role": char_row[2],
                        "description": char_row[3],
                        "background": char_row[4],
                        "goals": char_row[5],
                        "conflicts": char_row[6]
                    }
                
                # Busca os ambientes do capítulo
                cursor.execute("""
                    SELECT e.id, e.name, e.type, e.physical_description, e.atmosphere, 
                           e.important_elements, e.significance, e.suggestions
                    FROM environments e
                    JOIN chapter_environments ce ON e.id = ce.environment_id
                    WHERE ce.chapter_id = ?
                """, (chapter_id,))
                
                for env_row in cursor.fetchall():
                    env_id = env_row[0]
                    chapter["environments"][env_id] = {
                        "name": env_row[1],
                        "type": env_row[2],
                        "physical_description": env_row[3],
                        "atmosphere": env_row[4],
                        "important_elements": env_row[5],
                        "significance": env_row[6],
                        "suggestions": env_row[7]
                    }
                
                return chapter
        except Exception as e:
            print(f"Erro ao buscar capítulo: {e}")
            return None
    
    def save_timeline_event(self, event_data: Dict[str, Any]) -> str:
        """Salva um novo evento na linha do tempo."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                event_id = str(uuid.uuid4())
                
                cursor.execute("""
                    INSERT INTO timeline_events (
                        id, story_id, title, description, date, importance
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    event_id,
                    event_data.get("story_id"),
                    event_data.get("title"),
                    event_data.get("description"),
                    event_data.get("date"),
                    event_data.get("importance")
                ))
                
                conn.commit()
                return event_id
        except Exception as e:
            print(f"Erro ao salvar evento da linha do tempo: {e}")
            return None
    
    def get_timeline_events(self, story_id: str) -> List[Dict]:
        """Recupera todos os eventos da linha do tempo de uma história."""
        events = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM timeline_events
                WHERE story_id = ?
                ORDER BY chapter_number
            """, (story_id,))
            for row in cursor.fetchall():
                events.append({
                    "id": row[0],
                    "story_id": row[1],
                    "title": row[2],
                    "description": row[3],
                    "chapter": row[4]
                })
        return events
    
    def delete_character(self, char_id: str) -> bool:
        """Exclui um personagem e suas relações com capítulos."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Primeiro, exclui as relações com capítulos
                cursor.execute("DELETE FROM chapter_characters WHERE character_id = ?", (char_id,))
                
                # Depois, exclui o personagem
                cursor.execute("DELETE FROM characters WHERE id = ?", (char_id,))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao excluir personagem: {e}")
            return False

    def delete_environment(self, env_id: str) -> bool:
        """Deleta um ambiente do banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Primeiro remove as referências em chapter_environments
                cursor.execute("DELETE FROM chapter_environments WHERE environment_id = ?", (env_id,))
                # Depois remove o ambiente
                cursor.execute("DELETE FROM environments WHERE id = ?", (env_id,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar ambiente: {e}")
            return False

    def delete_chapter(self, chapter_id: str) -> bool:
        """Exclui um capítulo e suas relações com personagens e ambientes."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Primeiro, exclui as relações com personagens e ambientes
                cursor.execute("DELETE FROM chapter_characters WHERE chapter_id = ?", (chapter_id,))
                cursor.execute("DELETE FROM chapter_environments WHERE chapter_id = ?", (chapter_id,))
                
                # Depois, exclui o capítulo
                cursor.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao excluir capítulo: {e}")
            return False

    def delete_timeline_event(self, event_id: str) -> bool:
        """Exclui um evento da linha do tempo."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM timeline_events WHERE id = ?", (event_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao excluir evento da linha do tempo: {e}")
            return False

    def delete_story(self, story_id: str) -> bool:
        """Exclui uma história e todas suas relações do banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Primeiro, exclui os capítulos e suas relações
                cursor.execute("""
                    DELETE FROM chapter_characters
                    WHERE chapter_id IN (SELECT id FROM chapters WHERE story_id = ?)
                """, (story_id,))
                
                cursor.execute("""
                    DELETE FROM chapter_environments
                    WHERE chapter_id IN (SELECT id FROM chapters WHERE story_id = ?)
                """, (story_id,))
                
                cursor.execute("DELETE FROM chapters WHERE story_id = ?", (story_id,))
                
                # Depois, exclui os personagens e ambientes
                cursor.execute("DELETE FROM characters WHERE story_id = ?", (story_id,))
                cursor.execute("DELETE FROM environments WHERE story_id = ?", (story_id,))
                
                # Exclui os eventos da linha do tempo
                cursor.execute("DELETE FROM timeline_events WHERE story_id = ?", (story_id,))
                
                # Por fim, exclui a história
                cursor.execute("DELETE FROM stories WHERE id = ?", (story_id,))
                
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao excluir história: {e}")
            return False

    def get_current_story(self) -> Optional[Dict]:
        """Retorna a história mais recente com todos os seus dados relacionados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, title, description, genre, target_audience,
                           main_theme, narrative_style, setting
                    FROM stories
                    ORDER BY id DESC
                    LIMIT 1
                """)
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                story = {
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "genre": row[3],
                    "target_audience": row[4],
                    "main_theme": row[5],
                    "narrative_style": row[6],
                    "setting": row[7],
                    "characters": {},
                    "environments": {},
                    "chapters": {},
                    "timeline_events": {}
                }
                
                # Busca os personagens da história
                cursor.execute("""
                    SELECT id, name, role, description, background, goals, conflicts
                    FROM characters
                    WHERE story_id = ?
                """, (story["id"],))
                
                for char_row in cursor.fetchall():
                    char_id = char_row[0]
                    story["characters"][char_id] = {
                        "name": char_row[1],
                        "role": char_row[2],
                        "description": char_row[3],
                        "background": char_row[4],
                        "goals": char_row[5],
                        "conflicts": char_row[6]
                    }
                
                # Busca os ambientes da história
                cursor.execute("""
                    SELECT id, name, type, physical_description, atmosphere,
                           important_elements, significance, suggestions
                    FROM environments
                    WHERE story_id = ?
                """, (story["id"],))
                
                for env_row in cursor.fetchall():
                    env_id = env_row[0]
                    story["environments"][env_id] = {
                        "name": env_row[1],
                        "type": env_row[2],
                        "physical_description": env_row[3],
                        "atmosphere": env_row[4],
                        "important_elements": env_row[5],
                        "significance": env_row[6],
                        "suggestions": env_row[7]
                    }
                
                # Busca os capítulos da história
                cursor.execute("""
                    SELECT id, title, content
                    FROM chapters
                    WHERE story_id = ?
                    ORDER BY id
                """, (story["id"],))
                
                for chapter_row in cursor.fetchall():
                    chapter_id = chapter_row[0]
                    story["chapters"][chapter_id] = {
                        "title": chapter_row[1],
                        "content": chapter_row[2],
                        "characters": {},
                        "environments": {}
                    }
                    
                    # Busca os personagens do capítulo
                    cursor.execute("""
                        SELECT c.id, c.name, c.role, c.description, c.background, c.goals, c.conflicts
                        FROM characters c
                        JOIN chapter_characters cc ON c.id = cc.character_id
                        WHERE cc.chapter_id = ?
                    """, (chapter_id,))
                    
                    for char_row in cursor.fetchall():
                        char_id = char_row[0]
                        story["chapters"][chapter_id]["characters"][char_id] = {
                            "name": char_row[1],
                            "role": char_row[2],
                            "description": char_row[3],
                            "background": char_row[4],
                            "goals": char_row[5],
                            "conflicts": char_row[6]
                        }
                    
                    # Busca os ambientes do capítulo
                    cursor.execute("""
                        SELECT e.id, e.name, e.type, e.physical_description, e.atmosphere,
                               e.important_elements, e.significance, e.suggestions
                        FROM environments e
                        JOIN chapter_environments ce ON e.id = ce.environment_id
                        WHERE ce.chapter_id = ?
                    """, (chapter_id,))
                    
                    for env_row in cursor.fetchall():
                        env_id = env_row[0]
                        story["chapters"][chapter_id]["environments"][env_id] = {
                            "name": env_row[1],
                            "type": env_row[2],
                            "physical_description": env_row[3],
                            "atmosphere": env_row[4],
                            "important_elements": env_row[5],
                            "significance": env_row[6],
                            "suggestions": env_row[7]
                        }
                
                # Busca os eventos da linha do tempo
                cursor.execute("""
                    SELECT id, title, description, date, importance
                    FROM timeline_events
                    WHERE story_id = ?
                    ORDER BY date
                """, (story["id"],))
                
                for event_row in cursor.fetchall():
                    event_id = event_row[0]
                    story["timeline_events"][event_id] = {
                        "title": event_row[1],
                        "description": event_row[2],
                        "date": event_row[3],
                        "importance": event_row[4]
                    }
                
                return story
        except Exception as e:
            print(f"Erro ao buscar história atual: {e}")
            return None

    def get_all_stories(self) -> List[Dict]:
        """Retorna todas as histórias do banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, title, description, genre, target_audience,
                           main_theme, narrative_style, setting,
                           created_at, updated_at
                    FROM stories
                    ORDER BY created_at DESC
                """)
                rows = cursor.fetchall()
                return [{
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'genre': row[3],
                    'target_audience': row[4],
                    'main_theme': row[5],
                    'narrative_style': row[6],
                    'setting': row[7],
                    'created_at': row[8],
                    'updated_at': row[9]
                } for row in rows]
        except Exception as e:
            print(f"Erro ao buscar histórias: {e}")
            return []
    
    def get_book_characters(self, story_id: str) -> Dict[str, Dict]:
        """Retorna todos os personagens de uma história específica."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, role, description, background, goals, conflicts
                    FROM characters
                    WHERE story_id = ?
                    ORDER BY name
                """, (story_id,))
                
                characters = {}
                for row in cursor.fetchall():
                    char_id = row[0]
                    characters[char_id] = {
                        "name": row[1],
                        "role": row[2],
                        "description": row[3],
                        "background": row[4],
                        "goals": row[5],
                        "conflicts": row[6]
                    }
                
                return characters
        except Exception as e:
            print(f"Erro ao buscar personagens da história: {e}")
            return {}
    
    def get_book_environments(self, story_id: str) -> Dict[str, Dict]:
        """Retorna todos os ambientes de uma história específica."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, type, physical_description, atmosphere,
                           important_elements, significance, suggestions
                    FROM environments
                    WHERE story_id = ?
                    ORDER BY name
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
            print(f"Erro ao buscar ambientes da história: {e}")
            return {}
    
    def save_character_to_chapter(self, chapter_id: str, character_id: str) -> bool:
        """Salva a relação entre um personagem e um capítulo."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO chapter_characters (
                        chapter_id, character_id
                    ) VALUES (?, ?)
                """, (chapter_id, character_id))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao salvar relação entre personagem e capítulo: {e}")
            return False
    
    def save_environment_to_chapter(self, chapter_id: str, environment_id: str) -> bool:
        """Salva a relação entre um ambiente e um capítulo."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO chapter_environments (
                        chapter_id, environment_id
                    ) VALUES (?, ?)
                """, (chapter_id, environment_id))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao salvar relação entre ambiente e capítulo: {e}")
            return False
    
    def get_chapter_characters(self, chapter_id: str) -> Dict[str, Dict]:
        """Retorna todos os personagens de um capítulo específico."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT c.id, c.name, c.role, c.description, c.background, c.goals, c.conflicts
                    FROM characters c
                    JOIN chapter_characters cc ON c.id = cc.character_id
                    WHERE cc.chapter_id = ?
                    ORDER BY c.name
                """, (chapter_id,))
                
                characters = {}
                for row in cursor.fetchall():
                    char_id = row[0]
                    characters[char_id] = {
                        "name": row[1],
                        "role": row[2],
                        "description": row[3],
                        "background": row[4],
                        "goals": row[5],
                        "conflicts": row[6]
                    }
                
                return characters
        except Exception as e:
            print(f"Erro ao buscar personagens do capítulo: {e}")
            return {}
    
    def get_chapter_environments(self, chapter_id: str) -> Dict[str, Dict]:
        """Retorna todos os ambientes de um capítulo específico."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT e.id, e.name, e.type, e.physical_description, e.atmosphere,
                           e.important_elements, e.significance, e.suggestions
                    FROM environments e
                    JOIN chapter_environments ce ON e.id = ce.environment_id
                    WHERE ce.chapter_id = ?
                    ORDER BY e.name
                """, (chapter_id,))
                
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
            print(f"Erro ao buscar ambientes do capítulo: {e}")
            return {}
    
    def get_story_chapters(self, story_id: str) -> Dict[str, Dict]:
        """Retorna todos os capítulos de uma história específica."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, title, content
                    FROM chapters
                    WHERE story_id = ?
                    ORDER BY id
                """, (story_id,))
                
                chapters = {}
                for row in cursor.fetchall():
                    chapter_id = row[0]
                    chapters[chapter_id] = {
                        "title": row[1],
                        "content": row[2],
                        "characters": {},
                        "environments": {}
                    }
                    
                    # Busca os personagens do capítulo
                    cursor.execute("""
                        SELECT c.id, c.name, c.role, c.description, c.background, c.goals, c.conflicts
                        FROM characters c
                        JOIN chapter_characters cc ON c.id = cc.character_id
                        WHERE cc.chapter_id = ?
                    """, (chapter_id,))
                    
                    for char_row in cursor.fetchall():
                        char_id = char_row[0]
                        chapters[chapter_id]["characters"][char_id] = {
                            "name": char_row[1],
                            "role": char_row[2],
                            "description": char_row[3],
                            "background": char_row[4],
                            "goals": char_row[5],
                            "conflicts": char_row[6]
                        }
                    
                    # Busca os ambientes do capítulo
                    cursor.execute("""
                        SELECT e.id, e.name, e.type, e.physical_description, e.atmosphere,
                               e.important_elements, e.significance, e.suggestions
                        FROM environments e
                        JOIN chapter_environments ce ON e.id = ce.environment_id
                        WHERE ce.chapter_id = ?
                    """, (chapter_id,))
                    
                    for env_row in cursor.fetchall():
                        env_id = env_row[0]
                        chapters[chapter_id]["environments"][env_id] = {
                            "name": env_row[1],
                            "type": env_row[2],
                            "physical_description": env_row[3],
                            "atmosphere": env_row[4],
                            "important_elements": env_row[5],
                            "significance": env_row[6],
                            "suggestions": env_row[7]
                        }
                
                return chapters
        except Exception as e:
            print(f"Erro ao buscar capítulos da história: {e}")
            return {}
    
    def get_story_timeline_events(self, story_id: str) -> Dict[str, Dict]:
        """Retorna todos os eventos da linha do tempo de uma história específica."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, title, description, date, importance
                    FROM timeline_events
                    WHERE story_id = ?
                    ORDER BY date
                """, (story_id,))
                
                events = {}
                for row in cursor.fetchall():
                    event_id = row[0]
                    events[event_id] = {
                        "title": row[1],
                        "description": row[2],
                        "date": row[3],
                        "importance": row[4]
                    }
                
                return events
        except Exception as e:
            print(f"Erro ao buscar eventos da linha do tempo: {e}")
            return {}

    def update_chapter(self, chapter_data: Dict[str, Any]) -> bool:
        """Atualiza um capítulo existente no banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                chapter_id = chapter_data.get("id")
                
                # Atualiza os dados básicos do capítulo
                cursor.execute("""
                    UPDATE chapters
                    SET title = ?, content = ?
                    WHERE id = ?
                """, (
                    chapter_data.get("title"),
                    chapter_data.get("content"),
                    chapter_id
                ))
                
                # Atualiza os personagens do capítulo
                cursor.execute("DELETE FROM chapter_characters WHERE chapter_id = ?", (chapter_id,))
                for char_id in chapter_data.get("characters", []):
                    cursor.execute("""
                        INSERT INTO chapter_characters (
                            chapter_id, character_id
                        ) VALUES (?, ?)
                    """, (chapter_id, char_id))
                
                # Atualiza os ambientes do capítulo
                cursor.execute("DELETE FROM chapter_environments WHERE chapter_id = ?", (chapter_id,))
                for env_id in chapter_data.get("environments", []):
                    cursor.execute("""
                        INSERT INTO chapter_environments (
                            chapter_id, environment_id
                        ) VALUES (?, ?)
                    """, (chapter_id, env_id))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao atualizar capítulo: {e}")
            return False
    
    def update_timeline_event(self, event_data: Dict[str, Any]) -> bool:
        """Atualiza um evento existente na linha do tempo."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE timeline_events
                    SET title = ?, description = ?, date = ?, importance = ?
                    WHERE id = ?
                """, (
                    event_data.get("title"),
                    event_data.get("description"),
                    event_data.get("date"),
                    event_data.get("importance"),
                    event_data.get("id")
                ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao atualizar evento da linha do tempo: {e}")
            return False

    def update_story(self, story_data: Dict[str, Any]) -> bool:
        """Atualiza uma história existente no banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE stories SET
                        title = ?,
                        description = ?,
                        genre = ?,
                        target_audience = ?,
                        main_theme = ?,
                        narrative_style = ?,
                        setting = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (
                    story_data.get('title'),
                    story_data.get('description'),
                    story_data.get('genre'),
                    story_data.get('target_audience'),
                    story_data.get('main_theme'),
                    story_data.get('narrative_style'),
                    story_data.get('setting'),
                    story_data.get('id')
                ))
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar história: {e}")
            return False

    def update_character(self, character_data: Dict[str, Any]) -> bool:
        """Atualiza um personagem existente no banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE characters
                    SET name = ?, role = ?, description = ?, background = ?, goals = ?, conflicts = ?
                    WHERE id = ?
                """, (
                    character_data.get("name", ""),
                    character_data.get("role", ""),
                    character_data.get("description", ""),
                    character_data.get("background", ""),
                    character_data.get("goals", ""),
                    character_data.get("conflicts", ""),
                    character_data.get("id")
                ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao atualizar personagem: {e}")
            return False

    def get_timeline_event(self, event_id: str) -> Optional[Dict]:
        """Retorna um evento específico da linha do tempo."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, story_id, title, description, date, importance
                    FROM timeline_events
                    WHERE id = ?
                """, (event_id,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                return {
                    "id": row[0],
                    "story_id": row[1],
                    "title": row[2],
                    "description": row[3],
                    "date": row[4],
                    "importance": row[5]
                }
        except Exception as e:
            print(f"Erro ao buscar evento da linha do tempo: {e}")
            return None

    def update_environment(self, environment_data: Dict[str, Any]) -> bool:
        """Atualiza um ambiente existente no banco de dados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE environments
                    SET name = ?, type = ?, physical_description = ?,
                        atmosphere = ?, important_elements = ?,
                        significance = ?, suggestions = ?
                    WHERE id = ?
                """, (
                    environment_data.get("name"),
                    environment_data.get("type"),
                    environment_data.get("physical_description"),
                    environment_data.get("atmosphere"),
                    environment_data.get("important_elements"),
                    environment_data.get("significance"),
                    environment_data.get("suggestions"),
                    environment_data.get("id")
                ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao atualizar ambiente: {e}")
            return False 