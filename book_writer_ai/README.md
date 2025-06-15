# Assistente de Escrita de Livros

Esta é uma aplicação Streamlit que ajuda na criação e gerenciamento de livros, utilizando IA para gerar sugestões baseadas em descrições.

## Funcionalidades

- Criação de livros com sugestões geradas por IA (Gemini 2.0 Flash)
- Listagem de livros
- Edição de livros existentes
- Exclusão de livros
- Geração automática de ID único para cada livro

## Requisitos

- Python 3.8+
- Chave de API do Google (Gemini 2.0 Flash)

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` na raiz do projeto e adicione sua chave da API do Google:
```
GOOGLE_API_KEY=sua_chave_api_aqui
```

## Executando a aplicação

Para iniciar a aplicação, execute:
```bash
streamlit run app.py
```

## Uso

1. Acesse a aplicação no navegador (geralmente em http://localhost:8501)
2. Use a barra lateral para navegar entre as diferentes funcionalidades
3. Para criar um novo livro:
   - Digite uma descrição (opcional)
   - Clique em "Gerar Sugestões" para obter sugestões da IA
   - Preencha ou ajuste os campos conforme necessário
   - Clique em "Salvar Livro"

## Estrutura de Dados

Cada livro contém os seguintes campos:
- ID (gerado automaticamente)
- Título
- Volume
- Autor
- Gênero
- Idioma 