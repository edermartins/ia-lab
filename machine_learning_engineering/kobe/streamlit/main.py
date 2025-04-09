import streamlit as st
import pickle
import numpy as np
import mlflow
import mlflow.sklearn

st.markdown("""
# Kobe Bryant (Black Mamba)

Essa página tem como objetivo mostrar as previsões do modelo treinado para o lançamento de Kobe Bryant.

Para isso, é necessário informar os dados de produção, as previsões do modelo e o y_true.

"""
)

# Carregar o modelo de regressão logística do MLflow
mlflow.set_tracking_uri('http://localhost:5000')
modelo_uri = 'models:/logistic_regression_model/production'
modelo = mlflow.sklearn.load_model(modelo_uri)

# Interface do usuário para entrada de dados
st.sidebar.header('Dados do Arremesso')

distancia = st.sidebar.number_input('Distância do Arremesso (em metros)', min_value=0.0, max_value=30.0, step=0.1)
angulo = st.sidebar.number_input('Ângulo do Arremesso (em graus)', min_value=0.0, max_value=90.0, step=0.1)

# Botão para fazer a previsão
if st.sidebar.button('Verificar se acerta'):
    # Preparar os dados para o modelo
    dados = np.array([[distancia, angulo]])
    
    # Fazer a previsão
    previsao = modelo.predict(dados)
    
    # Exibir o resultado
    if previsao[0] == 1:
        st.success('Kobe acertaria o arremesso!')
    else:
        st.error('Kobe não acertaria o arremesso.')







