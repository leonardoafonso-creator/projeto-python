from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

def plot_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    save_path: str | Path | None = None,
) -> None:
    plt.figure(figsize=(8, 5))
    plt.bar(df[x], df[y])
    plt.title(title)
    plt.xlabel(xlabel if xlabel else x)
    plt.ylabel(ylabel if ylabel else y)
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()