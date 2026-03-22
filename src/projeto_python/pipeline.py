from pathlib import Path

import pandas as pd

from projeto_python.paths import DATA_RAW, DATA_PROCESSED, FIGURES_DIR, TABLES_DIR
from projeto_python.preprocessing import standardize_column_names, remove_empty_rows
from projeto_python.plotting import plot_bar
from projeto_python.stats import descriptive_summary, compare_two_groups_ttest


INPUT_FILE = DATA_RAW / "base_estudo.csv"


def load_data(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_column_names(df)
    df = remove_empty_rows(df)
    return df


def save_processed_data(df: pd.DataFrame) -> None:
    output_file = DATA_PROCESSED / "base_estudo_processada.csv"
    df.to_csv(output_file, index=False)
    print(f"Base processada salva em: {output_file}")


def save_descriptive_table(df: pd.DataFrame) -> None:
    numeric_df = df.select_dtypes(include="number")
    desc = descriptive_summary(numeric_df)
    output_file = TABLES_DIR / "tabela_descritiva.csv"
    desc.to_csv(output_file)
    print(f"Tabela descritiva salva em: {output_file}")


def save_group_means(df: pd.DataFrame) -> None:
    group_summary = (
        df.groupby("grupo")[["idade", "phq9", "gad7"]]
        .mean()
        .round(2)
    )
    output_file = TABLES_DIR / "medias_por_grupo.csv"
    group_summary.to_csv(output_file)
    print(f"Médias por grupo salvas em: {output_file}")


def save_group_plot(df: pd.DataFrame) -> None:
    plot_df = df.groupby("grupo", as_index=False)["phq9"].mean()

    output_file = FIGURES_DIR / "phq9_por_grupo.png"
    plot_bar(
        df=plot_df,
        x="grupo",
        y="phq9",
        title="PHQ-9 médio por grupo",
        xlabel="Grupo",
        ylabel="Média de PHQ-9",
        save_path=output_file,
    )
    print(f"Figura salva em: {output_file}")


def save_ttest_results(df: pd.DataFrame) -> None:
    result = compare_two_groups_ttest(
        df=df,
        group_col="grupo",
        value_col="phq9",
        group_a="Controle",
        group_b="Intervenção",
    )
    output_file = TABLES_DIR / "teste_t_phq9.csv"
    result.to_csv(output_file, index=False)
    print(f"Resultado do teste t salvo em: {output_file}")


def main() -> None:
    print(f"Lendo base: {INPUT_FILE}")
    df = load_data(INPUT_FILE)

    print("Limpando dados...")
    df = clean_data(df)

    save_processed_data(df)
    save_descriptive_table(df)
    save_group_means(df)
    save_group_plot(df)
    save_ttest_results(df)

    print("Pipeline concluído com sucesso.")


if __name__ == "__main__":
    main()