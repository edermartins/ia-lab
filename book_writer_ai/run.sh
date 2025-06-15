#!/bin/bash

# Configurar variáveis de ambiente
export BROWSER=none
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Executar o Streamlit
streamlit run run.py 