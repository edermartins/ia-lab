"""
This is a boilerplate pipeline 'separacao_dados'
generated using Kedro 0.19.12

Lê um dataset e separa em base de treino e base de teste
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from sklearn.model_selection import train_test_split
from .nodes import split_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs="data_filtered",
                outputs={
                    "train_data": "base_train",
                    "test_data": "base_test"
                },
                name="split_train_test_data",
            )
        ]
    )
