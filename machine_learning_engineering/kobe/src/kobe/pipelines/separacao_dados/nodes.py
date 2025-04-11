"""
This is a boilerplate pipeline 'separacao_dados'
generated using Kedro 0.19.12
"""
import pandas as pd
from sklearn.model_selection import train_test_split
import mlflow


def split_data(df: pd.DataFrame) -> dict:
    """
    Separa os dados em treino e teste (estratificada).
    
    Args:
        df: DataFrame com os dados a serem separados
        
    Returns:
        dict: Dicionário com os DataFrames de treino e teste
    """
    
    # Iniciando uma nova run do MLflow
    mlflow.set_experiment("Separacao de dados")
    with mlflow.start_run(run_name="separacao_dados"):
        # Assumindo que a coluna 'shot_made_flag' é nossa variável alvo
        X = df.drop('shot_made_flag', axis=1)
        y = df['shot_made_flag']
        
        test_size = 0.2
        random_state = 42
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state,
            stratify=y
        )
        
        # Reconstruindo os DataFrames completos
        train_df = pd.concat([X_train, y_train], axis=1)
        test_df = pd.concat([X_test, y_test], axis=1)
        
        # Registrando parâmetros no MLflow
        mlflow.log_param("test_size", test_size)
        mlflow.log_param("random_state", random_state)
        
        # Registrando métricas no MLflow
        mlflow.log_metric("tamanho_base_treino", len(train_df))
        mlflow.log_metric("tamanho_base_teste", len(test_df))
        
        return {
            "train_data": train_df,
            "test_data": test_df
        }