"""
This is a boilerplate pipeline 'preparacao_dados'
generated using Kedro 0.19.12
"""
from kedro.pipeline import node, Pipeline, pipeline  # noqa
import pandas as pd
import mlflow


def preparar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Função para preparar os dados do Kobe Bryant Shot Selection.
    
    Args:
        df: DataFrame com os dados brutos
        
    Returns:
        DataFrame processado com as featues e remove linhas com dados faltantes
    """
    # Iniciando uma nova run do MLflow
    with mlflow.start_run(run_name="preparacao_dados"):
        # Selecionando apenas as colunas necessárias
        colunas_selecionadas = ['lat', 'lon', 'minutes_remaining', 'period', 
                               'playoffs', 'shot_distance', 'shot_made_flag']
        
        df_filtrado = df[colunas_selecionadas].copy()
        
        # Registrando número de registros antes da limpeza
        num_registros_antes = len(df_filtrado)
        
        # Removendo registros com dados faltantes
        df_filtrado = df_filtrado.dropna()
        
        # Registrando número de registros após a limpeza
        num_registros_apos = len(df_filtrado)
        num_registros_removidos = num_registros_antes - num_registros_apos
        
        # Garantindo que shot_made_flag seja binário (0 ou 1)
        df_filtrado['shot_made_flag'] = df_filtrado['shot_made_flag'].astype(int)
        
        # Logando parâmetros e métricas no MLflow
        mlflow.log_param("colunas_selecionadas", colunas_selecionadas)
        mlflow.log_metric("num_registros_originais", num_registros_antes)
        mlflow.log_metric("num_registros_apos_limpeza", num_registros_apos)
        mlflow.log_metric("num_registros_removidos", num_registros_removidos)
        
        return df_filtrado