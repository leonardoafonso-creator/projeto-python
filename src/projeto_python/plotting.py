from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_bar_aggregated(
    df: pd.DataFrame,
    x: str,
    y: str,
    agg: str = "mean",
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    save_path: str | Path | None = None,
) -> None:
    if agg == "mean":
        plot_df = df.groupby(x, as_index=False)[y].mean()
    elif agg == "sum":
        plot_df = df.groupby(x, as_index=False)[y].sum()
    else:
        raise ValueError(f"Agregação não suportada: {agg}")

    plt.figure(figsize=(8, 5))
    plt.bar(plot_df[x], plot_df[y])
    plt.title(title)
    plt.xlabel(xlabel if xlabel else x)
    plt.ylabel(ylabel if ylabel else y)
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.close()


def plot_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    save_path: str | Path | None = None,
) -> None:
    plt.figure(figsize=(6, 5))
    plt.scatter(df[x], df[y])
    plt.title(title)
    plt.xlabel(xlabel if xlabel else x)
    plt.ylabel(ylabel if ylabel else y)
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.close()