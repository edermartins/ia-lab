# Assistente de Escrita de Livros

Esta é uma aplicação Streamlit que auxilia na criação, organização e edição de livros de ficção, com recursos de inteligência artificial (IA) para geração de sugestões de capítulos, personagens e ambientes. O sistema permite gerenciar livros, capítulos, personagens e ambientes, integrando IA generativa (Google Gemini) para auxiliar o escritor.

## Funcionalidades

- Criação, edição e exclusão de livros
- Criação, edição e exclusão de capítulos, com sugestões automáticas via IA
- Seleção de personagens e ambientes para cada capítulo
- Criação, edição e exclusão de personagens e ambientes
- Sugestão automática de personagens, ambientes e capítulos usando IA (Gemini 2.0 Flash)
- Organização dos capítulos por ordem
- Interface amigável via Streamlit

## Estrutura de Pastas

- `src/` — Código-fonte principal
  - `models/` — Modelos ORM (SQLAlchemy) para livros, capítulos, personagens e ambientes
  - `services/` — Serviços de acesso a dados e lógica de negócio
  - `interface/` — Interfaces de usuário (Streamlit) para livros, capítulos, personagens e ambientes
  - `agents/` — Agentes de sugestão baseados em IA (Langchain + Gemini)
  - `utils/` — Utilitários e logger
  - `database.py` — Inicialização e conexão com o banco de dados
- `logs/` — Logs da aplicação
- `tests/` — Testes automatizados
- `run.py` — Script principal para execução da aplicação
- `requirements.txt` — Dependências Python
- `run.sh` — Script de inicialização (opcional)

## Requisitos

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [SQLite3](https://www.sqlite.org/) (instale via `sudo apt install sqlite3` no Linux, ou equivalente para seu sistema)
- Chave de API do Google Gemini (Gemini 2.0 Flash)

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd <nome-da-pasta>
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Instale o SQLite3 (se ainda não estiver instalado):
   ```bash
   sudo apt install sqlite3
   ```
4. Crie um arquivo `.env` na raiz do projeto e adicione sua chave da API do Google:
   ```
   GOOGLE_API_KEY=sua_chave_api_aqui
   ```

## Executando a aplicação

Para iniciar a aplicação, execute:
```bash
streamlit run run.py
```

Acesse a aplicação no navegador em [http://localhost:8501](http://localhost:8501)

## Uso

- Utilize a barra lateral para navegar entre livros, personagens e ambientes.
- Clique em "Gerenciar Capítulos" para acessar e criar capítulos de um livro.
- Ao criar ou editar capítulos, use a sugestão de IA para preencher automaticamente os campos.
- Todos os dados são salvos em um banco SQLite local (`src/database.db`).

## Observações
- O sistema utiliza IA generativa (Google Gemini) para sugestões. Certifique-se de ter uma chave de API válida.
- O banco de dados é criado automaticamente na primeira execução.
- Para desenvolvimento, recomenda-se o uso de um ambiente virtual (venv ou conda).

---
