import pandas as pd

def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df

def remove_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(how="all").copy()