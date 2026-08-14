from datasets import load_dataset
import pandas as pd
from pathlib import Path


DATA_DIR = Path("data/hm")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def stream_transactions(limit: int = 1_000_000) -> pd.DataFrame:
    """
    Stream H&M transactions from Hugging Face and
    create a manageable local development dataset.
    """

    dataset = load_dataset(
        "einrafh/hnm-fashion-recommendations-data",
        "transactions",
        split="train",
        streaming=True,
    )

    rows = []

    for i, row in enumerate(dataset):

        rows.append(row)

        if i + 1 >= limit:
            break

        if (i + 1) % 100_000 == 0:
            print(f"Downloaded {i + 1:,} transactions")

    df = pd.DataFrame(rows)

    output_path = DATA_DIR / "transactions_sample.parquet"

    df.to_parquet(
        output_path,
        index=False,
    )

    print()
    print(f"Saved {len(df):,} transactions")
    print(f"Path: {output_path}")
    print(f"Shape: {df.shape}")

    return df


if __name__ == "__main__":
    stream_transactions(1_000_000)