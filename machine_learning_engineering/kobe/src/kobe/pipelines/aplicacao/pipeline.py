"""
This is a boilerplate pipeline 'aplicacao'
generated using Kedro 0.19.12
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import carregar_dados_producao, aplicar_modelo, registrar_resultados_mlflow


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=carregar_dados_producao,
                inputs="data_filtered",
                outputs=["dados_producao_preparados", "y_true_prod"],
                name="carregar_dados_producao_node",
            ),
            node(
                func=aplicar_modelo,
                inputs=["dados_producao_preparados", "modelo_treinado"],
                outputs=["dados_com_previsoes", "previsoes"],
                name="aplicar_modelo_node",
            ),
            node(
                func=registrar_resultados_mlflow,
                inputs=["dados_com_previsoes", "previsoes", "y_true_prod"],
                outputs="metricas_producao",
                name="registrar_resultados_mlflow_node",
            ),
        ]
    )
