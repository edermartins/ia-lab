"""
This is a boilerplate pipeline 'treinamento'
generated using Kedro 0.19.12

Pipeline de treinamento, treina um modelo de regressão logística e um modelo de árvore de decisão (de acordo com o exercício)
"""

import mlflow
import pandas as pd
from pycaret.classification import *
from sklearn.metrics import log_loss, f1_score, accuracy_score
import numpy as np

def train_logistic_regression(train_data: pd.DataFrame, test_data: pd.DataFrame) -> dict:
    """
    Treina um modelo de regressão logística usando PyCaret e registra métricas no MLflow
    """
    # Inicializa o ambiente PyCaret
    pycaret_setup = setup(data=train_data, target='shot_made_flag', session_id=42)
    
    # Treina o modelo de regressão logística
    lr_model = pycaret_setup.create_model('lr')

    tuned_lr_model = pycaret_setup.tune_model(lr_model, n_iter=100, optimize='AUC')
    
    # Faz previsões no conjunto de teste
    predictions = pycaret_setup.predict_model(tuned_lr_model, data=test_data)
    
    # Obtém as probabilidades usando o modelo diretamente
    X_test = test_data.drop('shot_made_flag', axis=1)
    probabilities = tuned_lr_model.predict_proba(X_test)
    accuracy = accuracy_score(test_data['shot_made_flag'], predictions['prediction_label'])
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
    mlflow.set_experiment("Treinamento")
    with mlflow.start_run(run_name="logistic_regression"):
        mlflow.log_metric("log_loss", log_loss_value)
        mlflow.log_metric("f1_score", f1_value) 
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_param("solver", tuned_lr_model.get_params()['solver'])
        mlflow.log_param("multi_class", tuned_lr_model.get_params()['multi_class'])

        mlflow.sklearn.log_model(tuned_lr_model, "logistic_regression_model", registered_model_name="LogisticRegressionModel")
    
    return {"model": tuned_lr_model, "log_loss": log_loss_value, "f1_score": f1_value}

def train_decision_tree(train_data: pd.DataFrame, test_data: pd.DataFrame) -> dict:
    """
    Treina um modelo de árvore de decisão usando PyCaret e registra métricas no MLflow
    """
    # Inicializa o ambiente PyCaret
    pycaret_setup = setup(data=train_data, target='shot_made_flag', session_id=42)
    
    # Treina o modelo de árvore de decisão
    dt_model = pycaret_setup.create_model('dt')

    # Tune do modelo de árvore de decisão
    tuned_dt_model = pycaret_setup.tune_model(dt_model, n_iter=100, optimize='AUC')
    
    # Faz previsões no conjunto de teste
    predictions = pycaret_setup.predict_model(tuned_dt_model, data=test_data)
    
    # Obtém as probabilidades usando o modelo diretamente
    X_test = test_data.drop('shot_made_flag', axis=1)
    probabilities = tuned_dt_model.predict_proba(X_test)
    accuracy = accuracy_score(test_data['shot_made_flag'], predictions['prediction_label'])
    
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
    mlflow.set_experiment("Treinamento")
    with mlflow.start_run(run_name="decision_tree"):
        mlflow.log_metric("log_loss", log_loss_value)
        mlflow.log_metric("f1_score", f1_value)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(tuned_dt_model, "decision_tree_model", registered_model_name="DecisionTreeModel")
    
    return {"model": tuned_dt_model, "log_loss": log_loss_value, "f1_score": f1_value}
