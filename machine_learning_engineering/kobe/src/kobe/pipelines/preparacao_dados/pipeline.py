"""
This is a boilerplate pipeline 'separacao_dados'
generated using Kedro 0.19.12

Pipeline de preparação de dados, seleciona as features e remove os dados faltantes
"""

from kedro.pipeline import node, Pipeline, pipeline
from .nodes import preparar_dados

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=preparar_dados,
            inputs="data_raw",
            outputs="data_filtered",
            name="preparar_dados_node",
        ),
    ]) 