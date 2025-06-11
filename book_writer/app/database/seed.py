from models import Database

def seed_database():
    """Popula o banco de dados com dados iniciais."""
    db = Database()
    
    # Seed de personagens
    characters = [
        {
            "name": "João Silva",
            "age": 25,
            "role": "Protagonista",
            "physical_traits": "Alto, magro, cabelos castanhos e olhos verdes",
            "personality": "Determinado, inteligente e um pouco teimoso",
            "background": "Filho de agricultores, sempre sonhou em ser escritor",
            "suggestions": "Pode ter um conflito interno sobre seguir seus sonhos ou ajudar a família"
        },
        {
            "name": "Maria Santos",
            "age": 28,
            "role": "Coadjuvante",
            "physical_traits": "Baixa, cabelos pretos longos, olhos castanhos",
            "personality": "Carinhosa, paciente e muito observadora",
            "background": "Professora de literatura, apaixonada por poesia",
            "suggestions": "Pode ser uma mentora para o protagonista"
        }
    ]
    
    # Seed de ambientes
    environments = [
        {
            "name": "Casa da Família Silva",
            "type": "Interior",
            "physical_description": "Casa simples no interior, com jardim e varanda",
            "atmosphere": "Acolhedora e familiar",
            "important_elements": "Biblioteca antiga, piano no canto da sala",
            "significance": "Local onde o protagonista cresceu e desenvolveu seu amor pela escrita",
            "suggestions": "Pode ser um local de conflito entre tradição e modernidade"
        },
        {
            "name": "Café Literário",
            "type": "Interior",
            "physical_description": "Café aconchegante com prateleiras de livros e mesas de madeira",
            "atmosphere": "Inspiradora e acolhedora",
            "important_elements": "Prateleiras de livros, piano ao vivo, mesas para leitura",
            "significance": "Local onde o protagonista encontra inspiração e conhece outros escritores",
            "suggestions": "Pode ser um ponto de encontro importante para a trama"
        }
    ]
    
    # Seed de história
    story = {
        "title": "O Escritor do Interior",
        "genre": "Drama",
        "synopsis": "A história de um jovem escritor que precisa escolher entre seguir seus sonhos ou ajudar sua família no interior",
        "suggestions": "Explorar o conflito entre tradição e modernidade, sonhos e responsabilidades"
    }
    
    # Salva os dados no banco
    for character in characters:
        db.save_character(character)
    
    for environment in environments:
        db.save_environment(environment)
    
    story_id = db.save_story(story)
    
    # Adiciona alguns capítulos
    chapters = [
        {
            "title": "O Sonho",
            "content": "João acorda cedo, como sempre, mas hoje é diferente. Ele tem uma ideia para um novo livro...",
            "chapter_number": 1,
            "characters": ["João Silva"],
            "environments": ["Casa da Família Silva"]
        },
        {
            "title": "O Encontro",
            "content": "No Café Literário, João conhece Maria, uma professora que mudará sua vida...",
            "chapter_number": 2,
            "characters": ["João Silva", "Maria Santos"],
            "environments": ["Café Literário"]
        }
    ]
    
    for chapter in chapters:
        db.save_chapter(story_id, chapter)
    
    # Adiciona eventos na linha do tempo
    timeline_events = [
        {
            "title": "Primeiro Rascunho",
            "description": "João começa a escrever seu novo livro",
            "chapter": 1
        },
        {
            "title": "Encontro no Café",
            "description": "João conhece Maria no Café Literário",
            "chapter": 2
        }
    ]
    
    for event in timeline_events:
        db.save_timeline_event(story_id, event)

if __name__ == "__main__":
    seed_database() 