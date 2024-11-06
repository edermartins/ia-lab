import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def kmeans(X, k, max_iter=300):
    """
    Implementação do algoritmo K-Means para a aula de Clustering

    Args:
        X: Matriz de dados com as amostras nas linhas e features nas colunas
        k: Número de clusters
        max_iter: Número máximo de iterações

    Returns:
        centroids: Matriz com os centroides finais
        labels: Vetor com as labels dos clusters para cada amostra
    """

    # Inicializa os centroides aleatoriamente
    n_samples, n_features = X.shape
    np.random.seed(0)
    centroids = X[np.random.choice(n_samples, k, replace=False)]

    for _ in range(max_iter):
        # Atribui cada amostra ao cluster mais próximo
        distances = np.sqrt(((X[:, np.newaxis, :] - centroids) ** 2).sum(axis=2))
        labels: object = np.argmin(distances, axis=1)

        # Calcula os novos centroides
        for i in range(k):
            centroids[i] = np.mean(X[labels == i], axis=0)

    return centroids, labels


# Carregar os dados
# Verifica se existe o arquivo local
url = './data/Country-data.csv'
if not os.path.isfile(url):
  # Caso contrário vai buscar no github publico
  url = 'https://raw.githubusercontent.com/edermartins/ia-lab/refs/heads/main/clustering/data/Country-data.csv'

# Cria o dataset
df = pd.read_csv(url)
# Cópia do dataset sem a variável texto 'country'
X_vars = df.drop(["country"],axis=1).copy()

# Normalização dos dados para a clusterização
scaler = StandardScaler()
df_scaled = scaler.fit_transform(X_vars)

# Aplica o K-Means feito na mão
result_centroids, result_labels = kmeans(df_scaled, 3)

# Visualiza os resultados
plt.scatter(df_scaled[:, 0], df_scaled[:, 1], c=result_labels, s=50, cmap='viridis')
plt.scatter(result_centroids[:, 0], result_centroids[:, 1], c='red', s=200, alpha=0.5)
plt.show()