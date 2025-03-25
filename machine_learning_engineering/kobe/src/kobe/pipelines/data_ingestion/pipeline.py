"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 0.19.12

FEITO APENAS PARA TESTES, POIS NÃO ESTAVA FUNCIONANDO IMPORTAR PARQUET
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import load_kobe_datasets


def create_pipeline(**kwargs) -> Pipeline:
    """Cria o pipeline de ingestão de dados.

    Returns:
        Pipeline: Pipeline configurado para ingestão de dados
    """
    return pipeline(
        [
            node(
                func=load_kobe_datasets,
                inputs=["dataset_kobe_dev", "dataset_kobe_prod"],
                outputs=["kobe_dev_data", "kobe_prod_data"],
                name="load_kobe_datasets_node",
            ),
        ]
    )
