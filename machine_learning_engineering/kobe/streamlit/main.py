import streamlit as st
import numpy as np
import mlflow
import mlflow.sklearn
import requests

st.markdown("""
# Kobe Bryant (Black Mamba)
## Eder Jani Martins

Essa página tem como objetivo mostrar as previsões do modelo treinado para o lançamento de Kobe Bryant.

Para isso, é necessário informar latitude, longitude, minutos restantes no quarto, período do jogo, se é playoffs e a distância do arremesso.

O modelo irá prever se Kobe acertou ou não o arremesso com base nessas informações.
"""
)

def call_inference(data):
    rows = [list(data.values())]

    response = requests.post(
        'http://localhost:5001/invocations', 
        json={
            'inputs': rows,
        }
    )
    inference = response.json()
    return inference['predictions'][0]

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
    dados =  {
        'latitude': lat,
        'longitude': lon,
        'minutes_remaining': minutes_remaining,
        'period': period,
        'playoffs': playoffs,
        'shot_distance': shot_distance
    }
    

    previsao = call_inference(dados)
    
    # Exibir o resultado
    if previsao == 1:
        st.success(f'Kobe acertou o arremesso!')
    else:
        st.error(f'Kobe não acertou o arremesso.')







