"""
This is a boilerplate pipeline 'treinamento'
generated using Kedro 0.19.12

Pipeline de treinamento, treina um modelo de regressão logística e um modelo de árvore de decisão (de acordo com o exercício)
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import train_logistic_regression, train_decision_tree


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=train_logistic_regression,
            inputs=["base_train", "base_test"],
            outputs="logistic_regression_results",
            name="train_logistic_regression_node",
        ),
        node(
            func=train_decision_tree,
            inputs=["base_train", "base_test"],
            outputs="decision_tree_results",
            name="train_decision_tree_node",
        ),
    ])
