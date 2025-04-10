"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

from kobe.pipelines.data_ingestion import create_pipeline as create_data_ingestion_pipeline
from kobe.pipelines.preparacao_dados import create_pipeline as create_preparacao_dados_pipeline
from kobe.pipelines.separacao_dados import create_pipeline as create_separacao_dados_pipeline
from kobe.pipelines.treinamento import create_pipeline as create_treinamento_pipeline
from kobe.pipelines.aplicacao import create_pipeline as create_aplicacao_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    data_ingestion_pipeline = create_data_ingestion_pipeline()
    preparacao_dados_pipeline = create_preparacao_dados_pipeline()
    separacao_dados_pipeline = create_separacao_dados_pipeline()
    treinamento_pipeline = create_treinamento_pipeline()
    aplicacao_pipeline = create_aplicacao_pipeline()

    pipelines = {
        "data_ingestion": data_ingestion_pipeline,
        "preparacao_dados": preparacao_dados_pipeline,
        "separacao_dados": separacao_dados_pipeline,
        "treinamento": treinamento_pipeline,
        "aplicacao": aplicacao_pipeline,
        "__default__": preparacao_dados_pipeline + separacao_dados_pipeline + treinamento_pipeline + aplicacao_pipeline,
    }

    return pipelines
