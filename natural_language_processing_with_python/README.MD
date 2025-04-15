Chegamos ao final da disciplina de Processamento de Linguagem Natural com Python. Ao longo das últimas aulas vimos uma série de aplicações que nos deram a amplitude de possibilidades em trabalhar com textos. Para tal, usamos diversas bibliotecas, onde as que mais se destacaram foram NLTK, SPACY e GENSIM. Chegou a hora de validar nosso conhecimento.

Faremos nosso projeto de disciplina em 2 etapas:

A primeira você irá realizar nesse notebook:
> [Git Hub - Profº Fernando Ferreira](https://gist.github.com/fernandoferreira-me/61e9e4a25060f95abbfdb8cb90aaaed9)

Você irá perceber que o código possui **lacunas** e você precisa completá-las (Normalmente denotadas por comentários "ESCREVA AQUI").


Abra o notebook no Colab notebook e complete o código para realizar a análise completa. O objetivo é separar notícias em português em 9 tópicos distintos. No fim, você irá gerar uma nuvem de palavras e outra nuvem de entidades para cada um dos tópicos.

Após a finalização do código, responda as questões relacionadas às competências:

**Implementar técnicas de lematização**

1. Qual o endereço do seu notebook (colab) executado? Use o botão de compartilhamento do colab para obter uma url.
2. Em qual célula está o código que realiza o download dos pacotes necessários para tokenização e stemming usando nltk?
3. Em qual célula está o código que atualiza o spacy e instala o pacote pt_core_news_lg?
4. Em qual célula está o download dos dados diretamente do kaggle?
5. Em qual célula está a criação do dataframe news_2016 (com examente 7943 notícias)?
6. Em qual célula está a função que tokeniza e realiza o stemming dos textos usando funções do nltk?
7. Em qual célula está a função que realiza a lematização usando o spacy?
8. Baseado nos resultados qual a diferença entre stemming e lematização, qual a diferença entre os dois procedimentos? Escolha quatro palavras para exemplificar.

**Construir um modelo de reconhecimento de entidades (NER) usando Spacy**

9. Em qual célula o modelo pt_core_news_lg está sendo carregado? Todos os textos do dataframe precisam ser analisados usando os modelos carregados. Em qual célula isso foi feito?
10. Indique a célula onde as entidades dos textos foram extraídas. Estamos interessados apenas nas organizações.
11. Cole a figura gerada que mostra a nuvem de entidades para cada tópico obtido (no final do notebook)

**Criar modelos utilizando vetorização de textos baseado em Bag of Words**

12. Quando adotamos uma estratégia frequentista para converter textos em vetores, podemos fazê-lo de diferentes maneiras. Mostramos em aula as codificações One-Hot, TF e TF-IDF. Explique a principal motivação em adotar TF-IDF frente as duas outras opções.
13. Indique a célula onde está a função que cria o vetor de TF-IDF para cada texto. 
14. Indique a célula onde estão sendo extraídos os tópicos usando o algoritmo de LDA.
15. Indique a célula onde a visualização LDAVis está criada.
16. Cole a figura com a nuvem de palavras para cada um dos 9 tópicos criados.
17. Escreva brevemente uma descrição para cada tópico extraído. Indique se você considera o tópico extraído semanticamente consistente ou não. 

**Criar modelos baseados em Word Embedding**

18. Neste projeto, usamos TF-IDF para gerar os vetores que servem de entrada para o algoritmo de LDA. Quais seriam os passos para gerar vetores baseados na técnica de Doc2Vec?
19. Em uma versão alternativa desse projeto, optamos por utilizar o algoritmo de K-Médias para gerar os clusters (tópicos). Qual das abordagens (TF-IDF ou Doc2Vec) seria mais adequada como processo de vetorização? Justifique com comentários sobre dimensionalidade e relação semântica entre documentos.
20. Leia o artigo "Introducing our Hybrid lda2vec Algorithm" (https://multithreaded.stitchfix.com/blog/2016/05/27/lda2vec/#topic=38&lambda=1&term=).
O algoritmo lda2vec pretende combinar o poder do word2vec com a interpretabilidade do algoritmo LDA. Em qual cenário o autor sugere que há benefícios para utilização deste novo algoritmo?

**Template de Rubrica para ser utilizado com a extensão Rubricator**

1. Implementar técnicas de lematização

    * O aluno fez o download dos pacotes stopwords, punkt e rslp?

    * O aluno baixou e atualizou a versão do spacy instalado no Colab e dos modelos em português?

    * O aluno criou uma conta no site kaggle.com para baixar os dados?

    * O aluno criou um novo dataframe news_2016 com os dados referentes ao ano de 2016 e da categoria "mercado" (total de 7943 notícias)?

    * O aluno realizou a tokenização de todos os textos usando word_tokenize da bibliteca nltk?

    * O aluno realizou o stemming usando RSLPStemmer?

    * O aluno realizou a lematização usando a biblioteca spacy?

    * O aluno explicou a diferença entre lematização e stemming?

2. Construir um modelo de reconhecimento de entidades (NER) usando Spacy

    * O aluno processou todos os textos com os modelos do spacy?

    * O aluno utilizou Spacy para extrair as entidades relacionadas?

    * O aluno filtrou as entidades apenas por organizações?

    * O aluno mostrou as entidades mais relevantes para cada tópico obtido?

3. Criar modelos utilizando vetorização de textos baseado em Bag of Words

    * O aluno explicou como a adoção de diferentes formas de vetorização impacta os modelos?

    * O aluno criou uma função que recebe tokens e converte para vetores TF-IDF?

    * O aluno utilizou o algoritmo LDA para extrair os tópicos do dataset?

    * O aluno gerou a visualização com a ferramenta LDAVis para interpretar os tópicos?

    * O aluno apresentou uma nuvem de palavras para cada tópico extraído?

    * O aluno forneceu uma interpretação para cada tópico extraído?

4. Criar modelos baseados em Word Embedding

    * O aluno descreveu os passos necessários para realizar uma vetorização de documentos baseado na técnica de embeddings?

    * O aluno apontou as diferenças entre usar a abordagem frequentista e baseada em modelos neurais?

    * O aluno indicou qual modelo é mais indicado para cada modelo?

    * O aluno explicou o modelo LDA2Vec?
