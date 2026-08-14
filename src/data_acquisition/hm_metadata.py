from datasets import load_dataset
import pandas as pd
from pathlib import Path


DATA_DIR = Path("data/hm")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def download_config(config_name: str, output_name: str):

    dataset = load_dataset(
        "einrafh/hnm-fashion-recommendations-data",
        config_name,
        split="train",
        streaming=True,
    )

    rows = []

    for i, row in enumerate(dataset):

        rows.append(row)

        if (i + 1) % 50_000 == 0:
            print(f"{config_name}: {i + 1:,} records")

    df = pd.DataFrame(rows)

    output_path = DATA_DIR / output_name

    df.to_parquet(
        output_path,
        index=False,
    )

    print(
        f"{config_name} saved: "
        f"{len(df):,} records -> {output_path}"
    )

    return df


if __name__ == "__main__":

    download_config(
        "articles",
        "articles.parquet",
    )

    download_config(
        "customers",
        "customers.parquet",
    )