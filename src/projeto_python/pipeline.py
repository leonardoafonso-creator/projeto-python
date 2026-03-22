from pathlib import Path

import pandas as pd

from projeto_python.config import load_yaml_config
from projeto_python.paths import CONFIG_DIR, DATA_RAW, DATA_PROCESSED, FIGURES_DIR, TABLES_DIR
from projeto_python.plotting import plot_bar_aggregated, plot_scatter
from projeto_python.preprocessing import (
    apply_variable_mapping,
    auto_standardize_columns,
    remove_empty_rows,
    validate_required_columns,
)
from projeto_python.stats import (
    descriptive_summary,
    group_summary,
    run_correlation,
    run_ttest,
)

CONFIG_FILE = CONFIG_DIR / "study_config.yaml"


def load_data(file_path: Path, sep: str = ",", encoding: str = "utf-8") -> pd.DataFrame:
    return pd.read_csv(file_path, sep=sep, encoding=encoding)


def clean_data(df: pd.DataFrame, mapping_file: Path, required_cols: list[str]) -> pd.DataFrame:
    df = auto_standardize_columns(df)

    mapping_df = pd.read_csv(mapping_file)
    df = apply_variable_mapping(df, mapping_df)

    df = remove_empty_rows(df)
    validate_required_columns(df, required_cols)

    return df


def main() -> None:
    config = load_yaml_config(CONFIG_FILE)

    input_file = DATA_RAW / config["input"]["file"]
    mapping_file = CONFIG_DIR / config["mapping"]["file"]

    group_col = config["variables"]["group"]
    numeric_cols = config["variables"]["numeric"]

    required_cols = [group_col] + numeric_cols

    print(f"Lendo base: {input_file}")
    df = load_data(
        file_path=input_file,
        sep=config["input"].get("sep", ","),
        encoding=config["input"].get("encoding", "utf-8"),
    )

    print("Limpando dados...")
    df = clean_data(df=df, mapping_file=mapping_file, required_cols=required_cols)

    processed_output = DATA_PROCESSED / config["outputs"]["processed_data"]
    df.to_csv(processed_output, index=False)
    print(f"Base processada salva em: {processed_output}")

    if config["analysis"].get("descriptive_table", False):
        desc = descriptive_summary(df[numeric_cols])
        desc_output = TABLES_DIR / config["outputs"]["descriptive_table"]
        desc.to_csv(desc_output)
        print(f"Tabela descritiva salva em: {desc_output}")

    if config["analysis"].get("group_summary", False):
        summary = group_summary(df, group_col=group_col, numeric_cols=numeric_cols)
        summary_output = TABLES_DIR / config["outputs"]["group_summary"]
        summary.to_csv(summary_output)
        print(f"Resumo por grupo salvo em: {summary_output}")

    stats_results = []

    if config["analysis"]["ttest"]["enabled"]:
        ttest_result = run_ttest(
            df=df,
            group_col=group_col,
            value_col=config["analysis"]["ttest"]["variable"],
            group_a=config["groups"]["reference"],
            group_b=config["groups"]["comparison"],
        )
        stats_results.append(ttest_result)

    if config["analysis"]["correlation"]["enabled"]:
        corr_result = run_correlation(
            df=df,
            x=config["analysis"]["correlation"]["x"],
            y=config["analysis"]["correlation"]["y"],
        )
        stats_results.append(corr_result)

    if stats_results:
        final_stats = pd.concat(stats_results, ignore_index=True)
        stats_output = TABLES_DIR / config["outputs"]["statistical_results"]
        final_stats.to_csv(stats_output, index=False)
        print(f"Resultados estatísticos salvos em: {stats_output}")

    if config["figures"]["barplot"]["enabled"]:
        bar_cfg = config["figures"]["barplot"]
        plot_bar_aggregated(
            df=df,
            x=bar_cfg["x"],
            y=bar_cfg["y"],
            agg=bar_cfg.get("agg", "mean"),
            title=bar_cfg.get("title", ""),
            xlabel=bar_cfg.get("xlabel", ""),
            ylabel=bar_cfg.get("ylabel", ""),
            save_path=FIGURES_DIR / bar_cfg["filename"],
        )
        print(f"Figura salva em: {FIGURES_DIR / bar_cfg['filename']}")

    if config["figures"]["scatter"]["enabled"]:
        scatter_cfg = config["figures"]["scatter"]
        plot_scatter(
            df=df,
            x=scatter_cfg["x"],
            y=scatter_cfg["y"],
            title=scatter_cfg.get("title", ""),
            xlabel=scatter_cfg.get("xlabel", ""),
            ylabel=scatter_cfg.get("ylabel", ""),
            save_path=FIGURES_DIR / scatter_cfg["filename"],
        )
        print(f"Figura salva em: {FIGURES_DIR / scatter_cfg['filename']}")

    print("Pipeline concluído com sucesso.")


if __name__ == "__main__":
    main()