import pandas as pd
from scipy.stats import ttest_ind


def descriptive_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe().T


def compare_two_groups_ttest(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    group_a: str,
    group_b: str,
) -> pd.DataFrame:
    values_a = df.loc[df[group_col] == group_a, value_col].dropna()
    values_b = df.loc[df[group_col] == group_b, value_col].dropna()

    t_stat, p_value = ttest_ind(values_a, values_b, equal_var=False)

    return pd.DataFrame(
        {
            "group_a": [group_a],
            "group_b": [group_b],
            "variable": [value_col],
            "t_stat": [t_stat],
            "p_value": [p_value],
        }
    )