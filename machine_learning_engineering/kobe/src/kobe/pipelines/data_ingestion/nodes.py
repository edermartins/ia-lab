"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 0.19.12

FEITO APENAS PARA TESTES, POIS NÃO ESTAVA FUNCIONANDO IMPORTAR PARQUET
"""
import pandas as pd
from typing import Tuple

def load_kobe_datasets(
    dataset_dev: pd.DataFrame,
    dataset_prod: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega os datasets de dev e prod.

    Args:
        dataset_dev: Dataset de dev
        dataset_prod: Dataset de prod

    Returns:
        Tuple contendo os datasets de dev e prod
    """
    return dataset_dev, dataset_prod

