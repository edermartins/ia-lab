import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.models import Database

def seed_database():
    """Adiciona dados iniciais ao banco de dados."""
    db = Database()
    
    # Cria uma história de exemplo
    story_data = {
        "title": "A Jornada do Escritor",
        "genre": "Ficção",
        "description": "Uma história sobre um escritor que descobre que seus personagens ganham vida.",
        "target_audience": "Adulto",
        "main_theme": "Criatividade e Realidade",
        "narrative_style": "Terceira Pessoa",
        "setting": "Uma pequena cidade no interior"
    }
    
    story_id = db.save_story(story_data)
    if not story_id:
        print("Erro ao criar história de exemplo.")
        return
    
    # Cria um personagem de exemplo
    character_data = {
        "story_id": story_id,
        "name": "João Silva",
        "role": "Protagonista",
        "description": "Um escritor em busca de inspiração",
        "background": "Ex-professor de literatura que decidiu seguir seu sonho de escrever",
        "goals": "Publicar seu primeiro livro",
        "conflicts": "Dúvidas sobre sua capacidade criativa"
    }
    
    character_id = db.save_character(character_data)
    if not character_id:
        print("Erro ao criar personagem de exemplo.")
        return
    
    # Cria um ambiente de exemplo
    environment_data = {
        "story_id": story_id,
        "name": "Casa de Campo",
        "type": "Residencial",
        "physical_description": "Uma antiga casa de madeira cercada por árvores",
        "atmosphere": "Acolhedora e misteriosa",
        "important_elements": "Uma máquina de escrever antiga",
        "significance": "Local onde a história principal se desenvolve",
        "suggestions": "Adicionar mais elementos místicos"
    }
    
    environment_id = db.save_environment(environment_data)
    if not environment_id:
        print("Erro ao criar ambiente de exemplo.")
        return
    
    # Cria um capítulo de exemplo
    chapter_data = {
        "story_id": story_id,
        "title": "O Primeiro Rascunho",
        "content": "João sentou-se em sua máquina de escrever, olhando para a página em branco..."
    }
    
    chapter_id = db.save_chapter(chapter_data)
    if not chapter_id:
        print("Erro ao criar capítulo de exemplo.")
        return
    
    # Cria um evento da linha do tempo
    event_data = {
        "story_id": story_id,
        "title": "A Descoberta",
        "description": "João descobre que seus personagens ganham vida",
        "date": "2024-03-20",
        "importance": "Alta"
    }
    
    event_id = db.save_timeline_event(event_data)
    if not event_id:
        print("Erro ao criar evento de exemplo.")
        return
    
    print("Dados iniciais adicionados com sucesso!")

if __name__ == "__main__":
    seed_database() 