"""
This is a boilerplate pipeline 'pipeline_aplicacao'
generated using Kedro 0.19.12
"""

import pandas as pd
import mlflow
import numpy as np
from sklearn.metrics import log_loss, f1_score
from typing import Tuple, Dict

def carregar_dados_producao(dados_producao: pd.DataFrame) -> pd.DataFrame:
    """
    Carrega e prepara os dados de produção
    """
    return dados_producao

def aplicar_modelo(
    dados_producao: pd.DataFrame,
    modelo: object
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Aplica o modelo nos dados de produção
    """
    # Faz as previsões
    probabilidades = modelo.predict_proba(dados_producao)
    previsoes = modelo.predict(dados_producao)
    
    # Adiciona as previsões ao DataFrame
    dados_producao['prediction'] = previsoes
    dados_producao['probability'] = probabilidades[:, 1]
    
    return dados_producao, previsoes

def registrar_resultados_mlflow(
    dados_producao: pd.DataFrame,
    previsoes: np.ndarray,
    y_true: np.ndarray
) -> Dict:
    """
    Registra os resultados no MLflow
    """
    # Calcula as métricas
    log_loss_score = log_loss(y_true, dados_producao['probability'])
    f1 = f1_score(y_true, previsoes)
    
    # Registra a run no MLflow
    with mlflow.start_run(run_name="PipelineAplicacao"):
        # Registra as métricas
        mlflow.log_metric("log_loss", log_loss_score)
        mlflow.log_metric("f1_score", f1)
        
        # Salva os resultados como artefato
        mlflow.log_artifact(
            "data/08_reporting/predictions_prod.parquet",
            "predictions_prod.parquet"
        )
    
    return {
        "log_loss": log_loss_score,
        "f1_score": f1
    }
