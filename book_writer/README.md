# Book Writer

Uma aplicação para auxiliar na escrita de livros, com recursos de geração de conteúdo usando IA.

## Funcionalidades

### Gerenciamento de Livros
- Criar novos livros
- Editar detalhes do livro (título, gênero, sinopse, etc.)
- Excluir livros e suas dependências
- Visualizar lista de livros

### Personagens
- Criar e editar personagens
- Definir características físicas e psicológicas
- Adicionar histórico e objetivos
- Excluir personagens
- Chat com personagens usando IA

### Ambientes
- Criar e editar ambientes
- Descrever características físicas
- Definir atmosfera e elementos importantes
- Excluir ambientes

### Capítulos
- Criar e editar capítulos
- Adicionar conteúdo
- Associar personagens e ambientes aos capítulos
- Excluir capítulos
- Gerar conteúdo de capítulos usando IA

### Linha do Tempo
- Criar e editar eventos
- Definir datas e importância
- Excluir eventos

### Geração de Conteúdo com IA
- Gerar sinopse do livro
- Gerar conteúdo de capítulos
- Sugerir ideias para personagens
- Chat interativo com personagens

## Requisitos

- Python 3.11+
- Conda
- Google Gemini API Key

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd book_writer
```

2. Crie e ative o ambiente conda:
```bash
conda create -n book_writer python=3.11
conda activate book_writer
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```
Edite o arquivo `.env` e adicione sua chave da API do Google Gemini:
```
GOOGLE_API_KEY=sua_chave_aqui
```

## Uso

### Iniciar a Aplicação
```bash
conda activate book_writer
streamlit run app/main.py
```

### Zerar o Banco de Dados
Para recriar o banco de dados do zero:
```bash
conda activate book_writer
rm book_writer.db
```
O banco de dados será recriado automaticamente na próxima execução da aplicação.

### Executar Seed (Dados Iniciais)
Para adicionar dados iniciais ao banco:
```bash
conda activate book_writer
python app/scripts/seed.py
```

## Estrutura do Projeto

```
book_writer/
├── app/
│   ├── components/         # Componentes da interface
│   ├── database/          # Modelos e operações do banco de dados
│   ├── scripts/           # Scripts utilitários
│   ├── utils/             # Utilitários e interfaces
│   └── main.py           # Ponto de entrada da aplicação
├── .env                   # Variáveis de ambiente
├── .env.example          # Exemplo de variáveis de ambiente
├── requirements.txt      # Dependências do projeto
└── README.md            # Este arquivo
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 