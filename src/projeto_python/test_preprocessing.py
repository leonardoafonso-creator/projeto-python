import pandas as pd

from projeto_python.preprocessing import standardize_column_names

def test_standardize_column_names() -> None:
    df = pd.DataFrame({"Coluna A": [1, 2], "Coluna B": [3, 4]})
    result = standardize_column_names(df)
    assert list(result.columns) == ["coluna_a", "coluna_b"]