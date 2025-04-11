import streamlit as st
import pickle
import numpy as np
import mlflow
import mlflow.sklearn

st.markdown("""
# Kobe Bryant (Black Mamba)
## Eder Jani Martins

Essa página tem como objetivo mostrar as previsões do modelo treinado para o lançamento de Kobe Bryant.

Para isso, é necessário informar latitude, longitude, minutos restantes no quarto, período do jogo, se é playoffs e a distância do arremesso.

O modelo irá prever se Kobe acertou ou não o arremesso com base nessas informações.
"""
)

# Carregar o modelo de regressão logística do MLflow
mlflow.set_tracking_uri('http://localhost:5000')
modelo_uri = 'runs:/0850e313316a4a29bf2c26bd8c72a04c/logistic_regression_model'
modelo = mlflow.sklearn.load_model(modelo_uri)

# Interface do usuário para entrada de dados
st.sidebar.header('Dados do Arremesso')

# Solicitar as features necessárias
lat = st.sidebar.number_input('Latitude (posição no campo)', format="%.4f", value=34.0413)
lon = st.sidebar.number_input('Longitude (posição no campo)', format="%.4f", value=-118.2318)
minutes_remaining = st.sidebar.number_input('Minutos restantes no quarto', min_value=0, max_value=20, step=1, value=8 )
period = st.sidebar.selectbox('Período do jogo', options=[1, 2, 3, 4, 5, 6, 7], index=0 )
playoffs = st.sidebar.selectbox('É playoffs?', options=[0, 1], index=0  )
shot_distance = st.sidebar.number_input('Distância do arremesso (em pés)', min_value=0, max_value=50, step=1, value=3)

# Botão para fazer a previsão
if st.sidebar.button('Verificar se acertou o arremesso'):
    # Preparar os dados para o modelo
    dados = np.array([[lat, lon, minutes_remaining, period, playoffs, shot_distance]])
    st.write(dados)
    
    # Fazer a previsão
    previsao = modelo.predict(dados)
    probabilidade = modelo.predict_proba(dados)[0][1]  # Probabilidade de acerto
    
    # Exibir o resultado
    if previsao[0] == 1:
        st.success(f'Kobe acertou o arremesso! (Probabilidade: {probabilidade:.2%})')
    else:
        st.error(f'Kobe não acertou o arremesso. (Probabilidade de acerto: {probabilidade:.2%})')







