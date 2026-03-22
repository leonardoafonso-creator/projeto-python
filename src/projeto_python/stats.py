import pandas as pd

def descriptive_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe().T