"""
This is a boilerplate pipeline 'treinamento'
generated using Kedro 0.19.12

Pipeline de treinamento, treina um modelo de regressão logística e um modelo de árvore de decisão (de acordo com o exercício)
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import train_logistic_regression, train_decision_tree, plot_roc_curve


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=train_logistic_regression,
            inputs=["base_train", "base_test", "params:session_id"],
            outputs="logistic_regression_model",
            name="train_logistic_regression_node",
        ),
        node(
            func=train_decision_tree,
            inputs=["base_train", "base_test", "params:session_id"],
            outputs="decision_tree_model",
            name="train_decision_tree_node",
        ),
        node(
            func=plot_roc_curve,
            inputs=[ "base_test", "logistic_regression_model", "params:session_id", "params:output_roc_curve_lr_path"],
            outputs=None,
            name="plot_roc_curve_lr_node",
        ),
        node(
            func=plot_roc_curve,
            inputs=[ "base_test", "decision_tree_model", "params:session_id", "params:output_roc_curve_dt_path"],
            outputs=None,
            name="plot_roc_curve_dt_node",
        ),
    ])
