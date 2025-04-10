# Matéria: Engenharia de Machine Learning [25E1_3]
## Aluno: Eder Jani Martins
## Data:11/04/2025

## Projeto disponível no Github

[https://github.com/edermartins/ia-lab/tree/main/machine_learning_engineering/kobe](https://github.com/edermartins/ia-lab/tree/main/machine_learning_engineering/kobe)


# Descrição do Projeto

Nesse momento, iremos validar todo nosso conhecimento sobre Engenharia de Machine Learning. Nós aprendemos neste curso a desenvolver coleta de dados, criar pipelines para processamento, adaptar modelos para operação e estabelecer métodos de atualização. Para tal, vimos conceitos como AutoML, MLOps, Visualização de Dados e estrutura de projetos. As questões a seguir irão abordar esses temas.

Para iniciar esta tarefa, baixe os dados que estão [localizados nesse link](https://www.kaggle.com/c/kobe-bryant-shot-selection/data). Esses são os dados dos arremessos realizados pelo astro da NBA Kobe Bryant durante sua carreira.

![imagem](./docs/kobe-every-shot-ever.png)
> **FIG 1**: Imagem retirada de: https://graphics.latimes.com/kobe-every-shot-ever/

# Enunciado

1. A solução criada nesse projeto deve ser disponibilizada em repositório git e disponibilizada em servidor de repositórios (Github (recomendado), Bitbucket ou Gitlab). O projeto deve obedecer o Framework TDSP da Microsoft (estrutura de arquivos, arquivo requirements.txt e arquivo README - com as respostas pedidas nesse projeto, além de outras informações pertinentes). Todos os artefatos produzidos deverão conter informações referentes a esse projeto (não serão aceitos documentos vazios ou fora de contexto). Escreva o link para seu repositório. 
> Em acordo com o professor Felipe Fink Grael, usaremos o padrão de pasta do Kedro
>
> Estrutura disponível no [github](https://github.com/edermartins/ia-lab/tree/main/machine_learning_engineering/kobe)


2. Iremos desenvolver um preditor de arremessos usando duas abordagens (regressão logística e classificação) para prever se o "Black Mamba" (apelido de Kobe) acertou ou errou a cesta.

    Baixe os dados de desenvolvimento e produção [aqui](https://github.com/tciodaro/eng_ml/tree/main/data) (datasets: `dataset_kobe_dev.parquet` e `dataset_kobe_prod.parquet`). Salve-os numa pasta `/data/raw` na raiz do seu repositório.
    > Os arquivos estão na pasta `data/01_raw`

    Para começar o desenvolvimento, desenhe um diagrama que demonstra todas as etapas necessárias para esse projeto, desde a aquisição de dados, passando pela criação dos modelos, indo até a operação do modelo.

3. Como as ferramentas Streamlit, MLFlow, PyCaret e Scikit-Learn auxiliam na construção dos pipelines descritos anteriormente? A resposta deve abranger os seguintes aspectos:

    * a. Rastreamento de experimentos;
    * b. Funções de treinamento;
    * c. Monitoramento da saúde do modelo;
    * d. Atualização de modelo;
    * f. Provisionamento (Deployment).

4. Com base no diagrama realizado na questão 2, aponte os artefatos que serão criados ao longo de um projeto. Para cada artefato, a descrição detalhada de sua composição.

### Descrição dos artefatos gerados

> * data/01_raw/data.csv: Base de dados baixada do Kaggle, conforme pedido no exercício
> * data/01_raw/dataset_kobe_dev.parquet: dados baixados do repositórios Githut, conforme pedido no exercício
> * data/01_raw/dataset_kobe_prod.parquet: dados baixados do repositórios Githut, conforme pedido no exercício
> * data/01_raw/y_true_prod.parquet: Dados reais de acertos (`shot_made_flag`) do arquivo `data/03_primary/dados_producao_preparados.parquet`, que é a base `data/01_raw/dataset_kobe_prod.parquet` sem os campos nulos
> * data/02_intermediate/data_filtered.parquet: aruqivo `data/01_raw/data.csv` sem os dados nulos
> * data/03_primary/base_test.parquet: 20% do aruqivo `data/02_intermediate/data_filtered.parquet` para teste
> * data/03_primary/base_train.parquet: 80% do aruqivo `data/02_intermediate/data_filtered.parquet` para treino
> * data/03_primary/dados_producao_preparados.parquet: É a base `data/01_raw/dataset_kobe_prod.parquet` sem os campos nulos
> * data/06_models/decision_tree_model.pkl: Árvore de decisão treinada
> * data/06_models/logistic_regression_model.pkl: Regressão logística treinada
> * data/08_reporting/metricas_producao.json: Métricas do treinamento
> * data/08_reporting/predictions_prod.parquet: Dados de previsão do modelo
> Pipelines:
> * src/kobe/pipelines/preparacao_dados: Pipeline + Node solititados no Item 5 de a. até b.
> * src/kobe/pipelines/separacao_dados: Pipeline + Node solititados no Item 5.b.vii
> * src/kobe/pipelines/treinamento: Pipeline + Node solititados no Item 6
> * src/kobe/pipelines/aplicacao: Pipeline + Node solititados no Item 7

5. Implemente o pipeline de processamento de dados com o mlflow, rodada (run) com o nome "PreparacaoDados":
* a. Os dados devem estar localizados em "`/data/raw/dataset_kobe_dev.parquet`" e "`/data/raw/dataset_kobe_prod.parquet`" 
* b. Observe que há dados faltantes na base de dados! As linhas que possuem dados faltantes devem ser desconsideradas. Para esse exercício serão apenas consideradas as colunas: 
  * i. lat
  * ii. lon
  * iii. minutes_remaining
  * iv. period
  * v. playoffs
  * vi. shot_distance

      A variável `shot_made_flag` será seu alvo, onde 0 indica que Kobe errou e 1 que a cesta foi realizada. O dataset resultante será armazenado na pasta "`/data/processed/data_filtered.parquet`". Ainda sobre essa seleção, qual a dimensão resultante do dataset?

  * vii. Separe os dados em treino (80%) e teste (20 %) usando uma escolha aleatória e estratificada. Armazene os datasets resultantes em "/Data/processed/base_{train|test}.parquet . Explique como a escolha de treino e teste afetam o resultado do modelo final. Quais estratégias ajudam a minimizar os efeitos de viés de dados.
> A escolha dos dados de treino e teste impacta diretamente a capacidade do modelo de aprender padrões reais e chegar numa boa generalização para dados novos. Um treino não pobre leva a overfifting ou underfitting. Já um teste inadequado fornece uma avaliação errada do desempenho. Viéses na divisão também podem distorcer a avaliação.

> Para minimizar o viés podemos fazer uma **amostragem estratificada**, que garante proporções de classes/variáveis importantes semelhantes nos conjuntos. Usar uma **amostragem aleatória**, que ajuda a reduzir o viés de seleção, dando igual chance a cada amostra. **Validação cruzada**, que é capaz de avaliar o modelo em múltiplas divisões, oferecendo uma estimativa mais robusta.
>
> Além disso temos que considerar o **tamanho adequado** de ambos os conjuntos, para que representem a variabilidade dos dados e garatir que os dados de treino e teste tenham distribuições semelhantes.


  * viii. Registre os parâmetros (% teste) e métricas (tamanho de cada base) no MlFlow
  > ![imagem](./docs/captura_5_viii.jpg)

6. Implementar o pipeline de treinamento do modelo com o MlFlow usando o nome "Treinamento"
   * a. Com os dados separados para treinamento, treine um modelo com regressão logística do sklearn usando a biblioteca pyCaret.
   * b. Registre a função custo "log loss" usando a base de teste
   * c. Com os dados separados para treinamento, treine um modelo de árvore de decisão do sklearn usando a biblioteca pyCaret.
   * d. Registre a função custo "log loss" e F1_score para o modelo de árvore.
   * e. Selecione um dos dois modelos para finalização e justifique sua escolha.

7. Registre o modelo de classificação e o sirva através do MLFlow (ou como uma API local, ou embarcando o modelo na aplicação). Desenvolva um pipeline de aplicação (`aplicacao.py`) para carregar a base de produção (`/data/raw/dataset_kobe_prod.parquet`) e aplicar o modelo. Nomeie a rodada (run) do mlflow como "PipelineAplicacao" e publique, tanto uma tabela com os resultados obtidos (artefato como `.parquet`), quanto log as métricas do novo log loss e f1_score do modelo.
   * a. O modelo é aderente a essa nova base? O que mudou entre uma base e outra? Justifique.
   > O modelo não é aderente à nova base. Apensar de dos campos `minutes_remaining`, `period`, `playoffs` e `shot_distance` serem similares e até iguais à base data.csv, os campos `lat` e `lon` são diferentes, fazendo o modelo errar e predizer muito mal.
   * b. Descreva como podemos monitorar a saúde do modelo no cenário com e sem a disponibilidade da variável resposta para o modelo em operação.
   * c. Descreva as estratégias reativa e preditiva de retreinamento para o modelo em operação.

8. Implemente um dashboard de monitoramento da operação usando Streamlit.

# Desenho da solução
![imagem](./docs/diagrama.png)

____
# Sessão com as respostas
Nesta sessão estão as soluções dos enunciados e as rúbricas solicitadas.

## Descrições do Dataset

A base de dados contém informações sobre os arremessos realizados por Kobe Bryant (Black Mamba), jogador da NBA. Abaixo está a descrição dos campos disponíveis na base de dados (baseado em deduções e pesquisas no Kaggle, nem todos os campos são óbvios). Cada linha é um arremesso:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| action_type | string | Tipo de ação do arremesso (ex: "Jump Shot", "Dunk", "Layup") |
| combined_shot_type | string | Tipo combinado do arremesso (ex: "Jump Shot", "Dunk", "Layup", "Hook Shot") |
| game_event_id | integer | ID único do evento no jogo |
| game_id | integer | ID único do jogo |
| lat | float | Latitude da posição do arremesso |
| loc_x | integer | Coordenada X da posição do arremesso |
| loc_y | integer | Coordenada Y da posição do arremesso |
| lon | float | Longitude da posição do arremesso |
| minutes_remaining | integer | Minutos restantes no período |
| period | integer | Período do jogo (1-4 para tempo regular, 5+ para prorrogação) |
| playoffs | integer | Indicador se o jogo é de playoffs, fase eliminatória da temporada (0 = não, 1 = sim) |
| season | string | Temporada do jogo (ex: "1996-97") |
| seconds_remaining | integer | Segundos restantes no período |
| shot_distance | float | Distância do arremesso em pés |
| shot_made_flag | integer | Resultado do arremesso (0 = errou, 1 = acertou) |
| shot_type | string | Tipo do arremesso (2 pontos "2PT Field Goal" ou 3 pontos "3PT Field Goal") |
| shot_zone_area | string | Área da quadra onde o arremesso foi realizado |
| shot_zone_basic | string | Área básica da quadra (ex: "Mid-Range", "In The Paint") |
| shot_zone_range | string | Faixa de distância do arremesso |
| team_id | integer | ID do time |
| team_name | string | Nome do time |
| game_date | string | Data do jogo |
| matchup | string | Confronto, código do time do Kobe vs código do time adversário (ex: "LAL vs. GSW") |
| opponent | string | Time adversário |
| shot_id | integer | ID único do arremesso |



# Template de Rubrica para apoiar a correção

1. Desenvolver um sistema de coleta de dados usando APIs públicas
* O aluno categorizou corretamente os dados?
> [Clique aqui para ver](#descrições-do-dataset)
* O aluno integrou a leitura dos dados corretamente à sua solução?
* O aluno aplicou o modelo em produção (servindo como API ou como solução embarcada)?
> O modelo foi servido via Mlflow [Clique aqui](#mlflow) para ver como executar o servidor e chamar a APO, disponível via URL.

* O aluno indicou se o modelo é aderente a nova base de dados?
> Após o treinamento com a base `data/01_raw/data.csv`, as predições utilizando a base `data/01_raw/dataset_kobe_prod.parquet` não foram boas. Obtive o `log_loss` = 0.6273682111956478 e `f1_score` = 0, o que indica que o modelo não conseguiu identificar nenhum elemento nessa base. 
>
> Isso pode ser visto no arquivo `data/08_reporting/predictions_prod.parquet`, onde todos os campos `prediction` estão em zero. Também observei que as probabilidades são bem baixas. O que indica que o modelo não é aderente á base de produção.
>
> Podemos ver no gráfico de importância de variáveis que latitude e longitude têm muita relevâvia. Isso fez o modelo não generalizar bem e ignorar as demais variáveis, que seriam muito mais relevante para prever os acertos:
![kobe_variable_importance.jpg](docs/kobe_variable_importance.jpg)

2. Criar uma solução de streaming de dados usando pipelines
* O aluno criou um repositório git com a estrutura de projeto baseado no Framework TDSP da Microsoft?
> Em acordo com o professor foi utilizado o padrão Kedro e está disponível na sessão [Projeto disponível no Github](#projeto-disponível-no-github)

* O aluno criou um diagrama que mostra todas as etapas necessárias para a criação de modelos?
> O diagrama pode ser visto [aqui](#desenho-da-solução)

* O aluno treinou um modelo de regressão usando PyCaret e MLflow?
> Foi criado no pipeline [Treinamento](https://github.com/edermartins/ia-lab/tree/main/machine_learning_engineering/kobe/src/kobe/pipelines/treinamento)

* O aluno calculou o Log Loss para o modelo de regressão e registrou no mlflow?
> Foi criado no pipeline [Treinamento](https://github.com/edermartins/ia-lab/tree/main/machine_learning_engineering/kobe/src/kobe/pipelines/treinamento)

* O aluno treinou um modelo de árvore de decisao usando PyCaret e MLflow?
> Foi criado no pipeline [Treinamento](https://github.com/edermartins/ia-lab/tree/main/machine_learning_engineering/kobe/src/kobe/pipelines/treinamento)

* O aluno calculou o Log Loss e F1 Score para o modelo de árvore de decisão e registrou no mlflow?
> Foi criado no pipeline [Treinamento](https://github.com/edermartins/ia-lab/tree/main/machine_learning_engineering/kobe/src/kobe/pipelines/treinamento)

3. Preparar um modelo previamente treinado para uma solução de streaming de dados
* O aluno indicou o objetivo e descreveu detalhadamente cada artefato criado no projeto?
> [Clique aqui para ver o resumo](#descrição-dos-artefatos-gerados)
* O aluno cobriu todos os artefatos do diagrama proposto?
> Todos os artefatos foram cobertos e estão disponíveis no [Github](https://github.com/edermartins/ia-lab/tree/main/machine_learning_engineering/kobe)

* O aluno usou o MLFlow para registrar a rodada "Preparação de Dados" com as métricas e argumentos relevantes?
> Pode ser visto no arquivo `nodes.py` do pipeline [Preparação do Dados](https://github.com/edermartins/ia-lab/tree/main/machine_learning_engineering/kobe/src/kobe/pipelines/preparacao_dados)

* O aluno removeu os dados faltantes da base?
> Pode ser visto no arquivo `nodes.py` do pipeline [Preparação do Dados](https://github.com/edermartins/ia-lab/tree/main/machine_learning_engineering/kobe/src/kobe/pipelines/preparacao_dados)

* O aluno selecionou as colunas indicadas para criar o modelo?
> Pode ser visto no arquivo `nodes.py` do pipeline [Preparação do Dados](https://github.com/edermartins/ia-lab/tree/main/machine_learning_engineering/kobe/src/kobe/pipelines/preparacao_dados)

* O aluno indicou quais as dimensões para a base preprocessada?
> Disponível nem `notebooks/dataset_analysis.ipynb`
> A base `data/01_raw/data.csv` tem (30697, 25) antes de ser limpa e (25697, 25) após a remoção dos campos nulos.
> 
> Já a base de `data/01_raw/dataset_kobe_prod.parquet` tem (6426, 25), antes de ser limpo e (5412, 7) após a remoção dos campos nulos.
> 
> Isso pode ser visto no notebook [dataset_analysis.ipynb](notebooks/dataset_analysis.ipynb)

* O aluno criou arquivos para cada fase do processamento e os armazenou nas pastas indicadas?
> Os arquivos de código e configuração podem ser vista no projeto do Github, mas os arquivos gerados não vão para o repositório mas se o projeto for executado os dados serão gerados. Também estou adicionando uma imagem demostrando minha pasta:

![imagem](./docs/data_files_screeshot.jpg)
* O aluno separou em duas bases, uma para treino e outra para teste?
> Foram criadas duas bases: `data/03_primary/base_train.parquet` e `data/03_primary/base_test.parquet`

* O aluno criou um pipeline chamado "Treinamento" no MlFlow?
> O pipeline de treinamento gera duas linhas no MLFlow: logistic_regression e decision_tree
![imagem](./docs/captura_pipeline_treinamento.jpg)

4. Estabelecer um método de como atualizar o modelo empregado em produção
* O aluno identificou a diferença entre a base de desenvolvimento e produção?
> Neste exercício a base utilizada para treinamento foi a `data/01_raw/data.csv`, que é bem grande, com 25.697 linhas e a base de produção `data/01_raw/dataset_kobe_prod.parquet` contem 5.412 registros. Isso faz sentido porque o modelo precisa de muito dados para aprender e generalizar bem. E os dados de produção, muitas vezes são menores ou até são disponibilizados uma por vez, via API.

* O aluno descreveu como monitorar a saúde do modelo no cenário com e sem a disponibilidade da variável alvo?
> Podemos monitorar um modelos de várias formas, inclusive vistas em matérias anteriores, através de métricas (acurácia, recall, f1 score, log loss, etc.). Também podemoa gerar uma curva AUC-ROC. Algumas dessas métricas e curvas podem ser vistas no notebook `notebooks/logistic_regression_and_decision_tree.ipynb`
>
> Caso a **variável alvo não esteja disponível**, podemo monitorar a distribuição de probabilidades previstas ao longo do tempo, analisar o drift nas cadasctetrísticas de entreda (features). Também podemo avaliar a estabilidade das previsões ou anomalias nas predições.

* O aluno implementou um dashboard de monitoramento da operação usando Streamlit?
> O projeto do strealit está em [streamlit/main.py](streamlit/main.py) e pode ser visto clicando [aqui](#streamlit)


* O aluno descreveu as estratégias reativa e preditiva de retreinamento para o modelo em operação?
> **Estratégia Reativa**: Monitoramento das métricas de desempenho (log loss, F1-score). Quando as métricas ultrapassarem um limite pré-definido ou alguma diferença estabelecida, o modelo é retreinado ou atualizar o modelo com dados recentes,
> 
> **Estratégia Preditiva**: Análisar as tendências e padrões nos dados de entrada. Periódicamente realizaer retreinamento baseado em sazonalidade ou mudanças esperadas. Também é possível implementar modelos de drift para detectar mudanças na distribuição dos dados antes que afetem o desempenho.

# MLFlow

## Como servir a última versão do modelo
Eu escolhi a Reguressão Logística que, no meu caso, está na versão 22

```
 mlflow models serve -m models:/LogisticRegressionModel/21 --env-manager=local --port 5001
```
### Como fazer uma chamada via API
Este exemplo mostra uma chamada para o servidor executando localmente:

```
curl --location 'http://localhost:5001/invocations' \
--data '{
    "inputs": [[34.0413, -118.2318, 8, 1, 0, 3]]
}'
```


# Streamlit

## Iniciando o Streamlit
O Streamlit vai iniciar na porta padrão (5000)

```
cd streamlit
streamlit run main.py
```
> ![docs/streamlit_kobe.jpg](docs/streamlit_kobe.jpg)
> Utilizando o modelo via Streamlit com a base ativa via Mlflow

_____
# Kedro Generated

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Overview

This is your new Kedro project with Kedro-Viz setup, which was generated using `kedro 0.19.12`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```
pip install -r requirements.txt
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the files `src/tests/test_run.py` and `src/tests/pipelines/data_science/test_pipeline.py` for instructions on how to write your tests. Run the tests as follows:

```
pytest
```

To configure the coverage threshold, look at the `.coveragerc` file.

## Project dependencies

To see and update the dependency requirements for your project use `requirements.txt`. Install the project requirements with `pip install -r requirements.txt`.

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can use tools like [`nbstripout`](https://github.com/kynan/nbstripout). For example, you can add a hook in `.git/config` with `nbstripout --install`. This will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

[Further information about using notebooks for experiments within Kedro projects](https://docs.kedro.org/en/develop/notebooks_and_ipython/kedro_and_notebooks.html).
## Package your Kedro project

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html).
