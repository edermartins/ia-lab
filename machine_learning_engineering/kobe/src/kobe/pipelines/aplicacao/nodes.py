"""
This is a boilerplate pipeline 'aplicacao'
generated using Kedro 0.19.12
"""

import pandas as pd
import mlflow
import numpy as np
from sklearn.metrics import log_loss, f1_score
from typing import Tuple, Dict

def carregar_dados_producao(dados_producao: pd.DataFrame, features: list) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carrega e prepara os dados de produção
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: DataFrame com os dados de produção e DataFrame com o y_true
    """
    # Removendo registros com dados faltantes
    dados_producao = dados_producao.dropna()

    # Extrai o shot_made_flag dos dados e converte num DataFrame
    y_true = pd.DataFrame({'shot_made_flag': dados_producao['shot_made_flag'].values})

    
    return dados_producao[features], y_true

def aplicar_modelo(
    dados_producao: pd.DataFrame,
    modelo: dict
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Aplica o modelo nos dados de produção
    """
    # Obtém o modelo do dicionário
    modelo_sklearn = modelo["model"]
    
    # Remove a coluna shot_made_flag se ela existir
    dados_para_previsao = dados_producao.copy()
    if 'shot_made_flag' in dados_para_previsao.columns:
        dados_para_previsao = dados_para_previsao.drop('shot_made_flag', axis=1)
    
    # Faz as previsões
    probabilidades = modelo_sklearn.predict_proba(dados_para_previsao)
    previsoes = modelo_sklearn.predict(dados_para_previsao)
    
    # Adiciona as previsões ao DataFrame original
    dados_producao['prediction'] = previsoes
    dados_producao['probability'] = probabilidades[:, 1]
    
    return dados_producao, previsoes

def registrar_resultados_mlflow(
    dados_producao: pd.DataFrame,
    previsoes: np.ndarray,
    y_true: pd.DataFrame
) -> Dict:
    """
    Registra os resultados no MLflow
        dados_producao: parquet com os dados de produção que consta no enunciado
        previsoes: Previsões do modelo treinado
        y_true: shot_made_flag dos dados de produção
    """
    # Calcula as métricas
    log_loss_score = log_loss(y_true['shot_made_flag'], dados_producao['probability'])
    f1_value = f1_score(y_true['shot_made_flag'], previsoes)
    
    # Registra a run no MLflow
    mlflow.set_experiment("Aplicação")
    with mlflow.start_run(run_name="aplicacao"):
        # Registra as métricas
        mlflow.log_metric("log_loss", log_loss_score)
        mlflow.log_metric("f1_score", f1_value)
        
        # Salva os resultados como artefato
        mlflow.log_artifact(
            "data/08_reporting/predictions_prod.parquet",
            "predictions_prod.parquet"
        )
    
    return {
        "log_loss": log_loss_score,
        "f1_score": f1_value
    }
