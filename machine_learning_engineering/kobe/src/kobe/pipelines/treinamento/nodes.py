"""
This is a boilerplate pipeline 'treinamento'
generated using Kedro 0.19.12

Pipeline de treinamento, treina um modelo de regressão logística e um modelo de árvore de decisão (de acordo com o exercício)
"""

import mlflow
import pandas as pd
from pycaret.classification import *
from sklearn.metrics import log_loss, f1_score
import numpy as np

def train_logistic_regression(train_data: pd.DataFrame, test_data: pd.DataFrame) -> dict:
    """
    Treina um modelo de regressão logística usando PyCaret e registra métricas no MLflow
    """
    # Inicializa o ambiente PyCaret
    clf = setup(data=train_data, target='shot_made_flag', session_id=42)
    
    # Treina o modelo de regressão logística
    lr_model = create_model('lr')
    
    # Faz previsões no conjunto de teste
    predictions = predict_model(lr_model, data=test_data)
    
    # Obtém as probabilidades usando o modelo diretamente
    X_test = test_data.drop('shot_made_flag', axis=1)
    probabilities = lr_model.predict_proba(X_test)
    
    # Debug detalhado
    print("\n=== Debug Regressão Logística ===")
    print("Colunas nas previsões:", predictions.columns.tolist())
    print("\nDistribuição das classes reais:")
    print(test_data['shot_made_flag'].value_counts(normalize=True))
    print("\nDistribuição das previsões:")
    print(predictions['prediction_label'].value_counts(normalize=True))
    print("\nProbabilidades:")
    print("Min:", probabilities.min())
    print("Max:", probabilities.max())
    print("Média:", probabilities.mean())
    print("Desvio padrão:", probabilities.std())
    
    # Calcula log loss usando as probabilidades da classe positiva
    log_loss_value = log_loss(test_data['shot_made_flag'], probabilities[:, 1])
    f1_value = f1_score(test_data['shot_made_flag'], predictions['prediction_label'])
    
    print("\nMétricas:")
    print("Log Loss:", log_loss_value)
    print("F1 Score:", f1_value)
    
    # Registra no MLflow
    mlflow.set_experiment("kobe_bryant_shots")
    with mlflow.start_run(run_name="logistic_regression"):
        mlflow.log_metric("log_loss", log_loss_value)
        mlflow.log_metric("f1_score", f1_value)
        mlflow.sklearn.log_model(lr_model, "logistic_regression_model")
    
    return {"model": lr_model, "log_loss": log_loss_value, "f1_score": f1_value}

def train_decision_tree(train_data: pd.DataFrame, test_data: pd.DataFrame) -> dict:
    """
    Treina um modelo de árvore de decisão usando PyCaret e registra métricas no MLflow
    """
    # Inicializa o ambiente PyCaret
    clf = setup(data=train_data, target='shot_made_flag', session_id=42)
    
    # Treina o modelo de árvore de decisão
    dt_model = create_model('dt')
    
    # Faz previsões no conjunto de teste
    predictions = predict_model(dt_model, data=test_data)
    
    # Obtém as probabilidades usando o modelo diretamente
    X_test = test_data.drop('shot_made_flag', axis=1)
    probabilities = dt_model.predict_proba(X_test)
    
    # Debug detalhado
    print("\n=== Debug Árvore de Decisão ===")
    print("Colunas nas previsões:", predictions.columns.tolist())
    print("\nDistribuição das classes reais:")
    print(test_data['shot_made_flag'].value_counts(normalize=True))
    print("\nDistribuição das previsões:")
    print(predictions['prediction_label'].value_counts(normalize=True))
    print("\nProbabilidades:")
    print("Min:", probabilities.min())
    print("Max:", probabilities.max())
    print("Média:", probabilities.mean())
    print("Desvio padrão:", probabilities.std())
    
    # Calcula métricas
    log_loss_value = log_loss(test_data['shot_made_flag'], probabilities[:, 1])
    f1_value = f1_score(test_data['shot_made_flag'], predictions['prediction_label'])
    
    print("\nMétricas:")
    print("Log Loss:", log_loss_value)
    print("F1 Score:", f1_value)
    
    # Registra no MLflow
    mlflow.set_experiment("kobe_bryant_shots")
    with mlflow.start_run(run_name="decision_tree"):
        mlflow.log_metric("log_loss", log_loss_value)
        mlflow.log_metric("f1_score", f1_value)
        mlflow.sklearn.log_model(dt_model, "decision_tree_model")
    
    return {"model": dt_model, "log_loss": log_loss_value, "f1_score": f1_value}
