# Use o comando abaixo ou importe via requirements.txt
# !pip install numpy pandas matplotlib scikit-learn seaborn scikit-learn-extra jupyter

# Importando as bibliotecas
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn_extra.cluster import KMedoids

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

# Mostra as primeiras linhas do dataset original
print(df.head())

# Exibindo o dataset normalizado
print("Dados normalizados:", df_scaled)

# Quantidade de países no dataset
num_paises = df['country'].nunique()
print("Total de países:", num_paises)

# Mostrar estatísticas descritivas para entender a faixa dinâmica das variáveis
print(df.describe())

# Verificando campos nulos e analisando a estrutura do dataset
print("Quantidade de campos nulos:", df.duplicated().sum())
df.info()

# Visualizando as variáveis de interesse
X_vars.hist(bins=15, figsize=(15, 10))
plt.show()

# Aplicando o Método do cotovelo (Elbow Method) > K-Média
elbow_graph=[]
for i in range(1,11):
    kmeans_result=KMeans(n_clusters=i, init='k-means++', random_state= 42)
    kmeans_result.fit(X_vars)
    elbow_graph.append(kmeans_result.inertia_)
plt.plot(range(1, 11), elbow_graph)
plt.title('Método do cotovelo (Elbow Method) > K-Means')
plt.xlabel('Número de Clusters')
plt.ylabel('Soma dos quadrados intra-clusters')
plt.xticks(range(1, 11))
plt.grid()
plt.show()

# Aplicando o Método do cotovelo (Elbow Method) > K-Medoide
elbow_graph=[]
for i in range(1,11):
    kMedoids_result=KMedoids(n_clusters=i, init='k-medoids++', random_state= 42)
    kMedoids_result.fit_predict(X_vars)
    elbow_graph.append(kMedoids_result.inertia_)
plt.plot(range(1, 11), elbow_graph)
plt.title('Método do cotovelo (Elbow Method) > K-Medoides')
plt.xlabel('Número de Clusters')
plt.ylabel('Soma dos quadrados intra-clusters')
plt.xticks(range(1, 11))
plt.grid()
plt.show()

# K-Médias
kmeans_result = KMeans(n_clusters=3, random_state=42)
y_vars = kmeans_result.fit_predict(df_scaled)
X_vars_kmeans = X_vars.copy()
X_vars_kmeans['Cluster_KMeans'] = kmeans_result.labels_

# Analisando a distribuição dos clusters (K-Médias)
cluster_counts = X_vars_kmeans['Cluster_KMeans'].value_counts()
print("Distribuição dos clusters (K-Médias):")
print(cluster_counts)

# Analisando a distribuição das dimensões em cada grupo (K-Médias)
cluster_means = X_vars_kmeans.groupby('Cluster_KMeans').mean()
print("Distribuição das dimensões em cada grupo (K-Médias):")
print(cluster_means)

# Clusterização Hierárquica através da função scipy.cluster.hierarchy.linkage do SciPy
linked = linkage(df_scaled, method='ward')

# Analisando a distribuição das dimensões em cada grupo (K-Médias)
cluster_means = X_vars_kmeans.groupby('Cluster_KMeans').mean()
print("Distribuição das dimensões em cada grupo (K-Médias):")
print(cluster_means)

# Exibir os países que representam cada cluster (K-Médias)
def calcular_pais_representativo(cluster_num, df, df_scaled, kmeans):
    # Gera um índice do cluster n
    cluster_indices = df[X_vars_kmeans['Cluster_KMeans'] == cluster_num].index
    # Resupera o elementro central de cada cluster, procurando o mais próximo através da distãncia do centro
    cluster_center = kmeans_result.cluster_centers_[cluster_num]
    distancias = np.linalg.norm(df_scaled[cluster_indices] - cluster_center, axis=1)
    pais_representativo_idx = cluster_indices[np.argmin(distancias)]
    return df.loc[pais_representativo_idx, 'country']

for cluster_num in range(3):
    pais_representativo = calcular_pais_representativo(cluster_num, df, df_scaled, kmeans_result)
    print(f"Cluster {cluster_num} é melhor representado por: {pais_representativo}")
    
# Dendograma
plt.figure(figsize=(65, 14))
plt.rcParams.update({'font.size': 30})
dendrogram(linked, labels=df['country'].values, leaf_rotation=90, leaf_font_size=20)
plt.title('Dendograma da Clusterização Hierárquica', fontsize=30)
plt.xlabel('Países', fontsize=30)
plt.ylabel('Distância Euclidiana', fontsize=30)
plt.show()

# Medóide
kmedoids_result = KMedoids(n_clusters=3, random_state=42)
y_vars_m = kmedoids_result.fit_predict(df_scaled)
X_vars['Cluster_Medoid'] = kmedoids_result.labels_

# Analisando a distribuição dos clusters (K-Medoides)
cluster_counts = X_vars['Cluster_Medoid'].value_counts()
print("Distribuição dos clusters (K-Medóide):")
print(cluster_counts)

# Analisando a distribuição das dimensões em cada grupo (K-Medoides)
cluster_means = X_vars.groupby('Cluster_Medoid').mean()
print("Distribuição das dimensões em cada grupo (K-Medóide):")
print(cluster_means)

# Visualizando o resultado do K-Média
X = df_scaled
plt.scatter(X[y_vars == 0, 0], X[y_vars == 0, 4], s = 100, c = 'blue', label = 'Cluster 1')
plt.scatter(X[y_vars == 1, 0], X[y_vars == 1, 4], s = 100, c = 'green', label = 'Cluster 2')
plt.scatter(X[y_vars == 2, 0], X[y_vars == 2, 4], s = 100, c = 'red', label = 'Cluster 3')
plt.scatter(kmeans_result.cluster_centers_[:, 0], kmeans_result.cluster_centers_[:, 2], s = 300, c = 'black', label = 'Centroid') # modificado
plt.rcParams.update({'font.size': 12})
plt.title('K-Média - Clusters (base normalizada)')
plt.xlabel('Motalidade infantil')
plt.ylabel('Renda anual')
plt.legend()
plt.show()

# Visualizando o resultado
X = df_scaled
plt.scatter(X[y_vars_m == 0, 0], X[y_vars_m == 0, 4], s = 100, c = 'green', label = 'Cluster 1')
plt.scatter(X[y_vars_m == 1, 0], X[y_vars_m == 1, 4], s = 100, c = 'red', label = 'Cluster 2')
plt.scatter(X[y_vars_m == 2, 0], X[y_vars_m == 2, 4], s = 100, c = 'blue', label = 'Cluster 3')
plt.scatter(kmedoids_result.cluster_centers_[:, 0], kmedoids_result.cluster_centers_[:, 2], s = 300, c = 'black', label = 'Medoide') # modificado
plt.rcParams.update({'font.size': 12})
plt.title('K-Medoide - Clusters (base normalizada)')
plt.xlabel('Motalidade infantil')
plt.ylabel('Renda anual')
plt.legend()
plt.show()