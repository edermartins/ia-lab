# Book Writer - Assistente de Escrita com IA

Este é um aplicativo interativo que utiliza IA para auxiliar na escrita de livros. O sistema utiliza Streamlit para a interface, Google Gemini como LLM principal (com suporte para troca de LLMs) e LangChain para orquestração.

## Funcionalidades Principais

- Criação e gerenciamento de personagens com perfis de IA
- Desenvolvimento de ambientes e cenários
- Geração de diálogos entre personagens
- Controle de linha do tempo e continuidade da história
- Revisão e coerência do conteúdo
- Interface interativa com chat para cada elemento do livro

## Arquitetura

O aplicativo é construído com:

- **Streamlit**: Interface do usuário e interatividade
- **Google Gemini**: Modelo de linguagem principal
- **LangChain**: Framework para orquestração de LLMs e agentes
- **Agentes de IA**: Personagens, ambientes e controladores de história

## Estrutura do Projeto

```
book_writer/
├── app/
│   ├── main.py
│   ├── agents/
│   │   ├── character_agent.py
│   │   ├── environment_agent.py
│   │   └── story_controller.py
│   ├── components/
│   │   ├── character_editor.py
│   │   ├── environment_editor.py
│   │   └── story_editor.py
│   └── utils/
│       ├── llm_interface.py
│       └── config.py
├── requirements.txt
└── README.md
```

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas chaves de API
```

## Execução

Para iniciar o aplicativo:

```bash
streamlit run app/main.py
```

## Uso

1. Acesse a interface web através do navegador
2. Comece criando seus personagens e definindo seus perfis
3. Desenvolva os ambientes e cenários
4. Use o chat interativo para refinar cada elemento
5. Gere diálogos e cenas usando os agentes de IA
6. Revise e mantenha a coerência da história

## Contribuição

Contribuições são bem-vindas! Por favor, leia as diretrizes de contribuição antes de submeter pull requests. 