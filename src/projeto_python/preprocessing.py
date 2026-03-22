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


def auto_standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns
        .str.lower()
        .str.replace("-", "", regex=False)
        .str.replace("_", "", regex=False)
        .str.replace(" ", "", regex=False)
    )
    return df


def apply_variable_mapping(df: pd.DataFrame, mapping_df: pd.DataFrame) -> pd.DataFrame:
    mapping_df = mapping_df.copy()

    mapping_df["original_name"] = (
        mapping_df["original_name"]
        .astype(str)
        .str.lower()
        .str.replace("-", "", regex=False)
        .str.replace("_", "", regex=False)
        .str.replace(" ", "", regex=False)
    )

    mapping_dict = dict(zip(mapping_df["original_name"], mapping_df["standard_name"]))
    df = df.rename(columns=mapping_dict)
    return df


def remove_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(how="all").copy()


def validate_required_columns(df: pd.DataFrame, required_cols: list[str]) -> None:
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")