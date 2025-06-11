import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do LLM
LLM_CONFIG = {
    "model": os.getenv("LLM_MODEL", "gemini-pro"),
    "temperature": float(os.getenv("TEMPERATURE", "0.7")),
    "max_tokens": int(os.getenv("MAX_TOKENS", "2048"))
}

# Configurações do Streamlit
STREAMLIT_CONFIG = {
    "server_port": int(os.getenv("STREAMLIT_SERVER_PORT", "8501")),
    "server_address": os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")
}

# Configurações do projeto
PROJECT_CONFIG = {
    "name": "Book Writer",
    "version": "1.0.0",
    "description": "Assistente de escrita de livros com IA"
}

# Configurações de armazenamento
STORAGE_CONFIG = {
    "characters_file": "data/characters.json",
    "environments_file": "data/environments.json",
    "story_file": "data/story.json"
}

# Configurações de prompts
PROMPT_CONFIG = {
    "character_generation": """
    Crie um perfil detalhado para um personagem de livro com as seguintes informações:
    Nome: {name}
    Papel: {role}
    
    Por favor, forneça:
    1. Descrição física detalhada
    2. Traços de personalidade
    3. Histórico e motivações
    """,
    
    "environment_generation": """
    Crie uma descrição detalhada para um ambiente de livro com as seguintes informações:
    Nome: {name}
    Tipo: {type}
    
    Por favor, forneça:
    1. Descrição física detalhada
    2. Atmosfera e clima
    3. Elementos importantes
    4. Significado na história
    """,
    
    "chapter_generation": """
    Crie o conteúdo para um capítulo de livro com as seguintes informações:
    Título do Capítulo: {title}
    
    Personagens presentes:
    {characters}
    
    Ambientes:
    {environments}
    
    Por favor, crie um capítulo envolvente que desenvolva a história e os personagens.
    """,
    
    "coherence_analysis": """
    Analise a coerência da seguinte história e forneça sugestões de melhoria:
    {story_data}
    
    Verifique:
    1. Consistência da trama
    2. Desenvolvimento dos personagens
    3. Uso dos ambientes
    4. Continuidade da linha do tempo
    5. Coerência com o gênero
    """
} 