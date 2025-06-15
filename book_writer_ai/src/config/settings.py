import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GEMINI_MODEL = 'gemini-2.0-flash'

# Configurações do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///books.db')

# Configurações da aplicação
APP_NAME = "Book Writer AI"
APP_ICON = "📚"

# Configurações de templates
SUGGESTION_TEMPLATE = """
Você é um assistente especializado em criar sugestões de livros. Com base na descrição fornecida, crie uma sugestão detalhada de livro.

Descrição: {description}

Retorne APENAS um objeto JSON válido contendo uma lista de sugestões de livros. Cada sugestão deve ter os seguintes campos:
- titulo: título do livro
- volume: número do volume (se aplicável)
- autor: nome do autor
- genero: gênero literário
- idioma: idioma do livro
- sinopse: breve descrição do enredo
- estilo_narrativo: estilo de narração (ex: primeira pessoa, terceira pessoa, epistolar, etc.)
- publico_alvo: público alvo do livro (ex: infantil, juvenil, adulto, etc.)

Exemplo de formato:
[
    {{
        "titulo": "O Nome do Livro",
        "volume": "1",
        "autor": "Nome do Autor",
        "genero": "Ficção Científica",
        "idioma": "Português",
        "sinopse": "Uma breve descrição do enredo...",
        "estilo_narrativo": "Terceira pessoa",
        "publico_alvo": "Juvenil"
    }}
]

Regras importantes:
1. Use aspas duplas para strings
2. Não use vírgula após o último item
3. Não inclua texto adicional ou formatação markdown
4. Não use blocos de código
5. Retorne apenas o JSON válido
"""

# Configuração da API do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Template para sugestão de personagens
CHARACTER_SUGGESTION_TEMPLATE = """
Você é um assistente especializado em criar sugestões de personagens. Com base na descrição fornecida, crie uma sugestão detalhada de personagem.

Descrição: {description}

Retorne APENAS um objeto JSON válido contendo uma lista de sugestões de personagens. Cada sugestão deve ter os seguintes campos:
- nome: nome do personagem
- idade: idade do personagem
- papel: papel do personagem na história
- caracteristicas_fisicas: descrição física do personagem
- personalidade: traços de personalidade
- historico: histórico e background do personagem

Exemplo de formato:
[
    {{
        "nome": "Nome do Personagem",
        "idade": 25,
        "papel": "Protagonista",
        "caracteristicas_fisicas": "Descrição física detalhada...",
        "personalidade": "Traços de personalidade...",
        "historico": "Histórico e background..."
    }}
]

Regras importantes:
1. Use aspas duplas para strings
2. Não use vírgula após o último item
3. Não inclua texto adicional ou formatação markdown
4. Não use blocos de código
5. Retorne apenas o JSON válido
"""

# Template para sugestão de ambientes
ENVIRONMENT_SUGGESTION_TEMPLATE = """
Você é um assistente especializado em criar sugestões de ambientes e cenários. Com base na descrição fornecida, crie uma sugestão detalhada de ambiente.

Descrição: {description}

Retorne APENAS um objeto JSON válido contendo uma lista de sugestões de ambientes. Cada sugestão deve ter os seguintes campos:
- nome: nome do ambiente
- tipo: tipo de ambiente (ex: floresta, cidade, castelo, etc.)
- descricao: descrição detalhada do ambiente
- atmosfera: atmosfera e clima do ambiente
- elementos_importantes: elementos e objetos importantes no ambiente
- significado: significado simbólico ou importância do ambiente na história

Exemplo de formato:
[
    {{
        "nome": "Nome do Ambiente",
        "tipo": "Tipo do Ambiente",
        "descricao": "Descrição detalhada do ambiente...",
        "atmosfera": "Descrição da atmosfera e clima...",
        "elementos_importantes": "Lista de elementos importantes...",
        "significado": "Significado e importância do ambiente..."
    }}
]

Regras importantes:
1. Use aspas duplas para strings
2. Não use vírgula após o último item
3. Não inclua texto adicional ou formatação markdown
4. Não use blocos de código
5. Retorne apenas o JSON válido
""" 