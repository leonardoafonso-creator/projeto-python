import pandas as pd
from scipy.stats import pearsonr, ttest_ind


def descriptive_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe().T


def group_summary(df: pd.DataFrame, group_col: str, numeric_cols: list[str]) -> pd.DataFrame:
    return df.groupby(group_col)[numeric_cols].agg(["mean", "std"]).round(2)


def run_ttest(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    group_a: str,
    group_b: str,
) -> pd.DataFrame:
    values_a = df.loc[df[group_col] == group_a, value_col].dropna()
    values_b = df.loc[df[group_col] == group_b, value_col].dropna()

    t_stat, p_value = ttest_ind(values_a, values_b, equal_var=False)

    return pd.DataFrame({
        "analysis": ["ttest"],
        "variable": [value_col],
        "group_a": [group_a],
        "group_b": [group_b],
        "statistic": [t_stat],
        "p_value": [p_value],
    })


def run_correlation(df: pd.DataFrame, x: str, y: str) -> pd.DataFrame:
    valid = df[[x, y]].dropna()
    r, p_value = pearsonr(valid[x], valid[y])

    return pd.DataFrame({
        "analysis": ["correlation"],
        "x": [x],
        "y": [y],
        "statistic": [r],
        "p_value": [p_value],
    })