import os
import pandas as pd
import numpy as np

from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors


INTERACTION_FILE = "data/features/interactions"
OUTPUT_DIR = "data/models"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "item_similarity_topk.parquet"
)

TOP_K = 20


def load_interactions():
    print("Loading interactions...")

    df = pd.read_parquet(INTERACTION_FILE)

    print(f"Loaded {len(df):,} interactions")
    print(f"Users: {df['customer_id'].nunique():,}")
    print(f"Items: {df['article_id'].nunique():,}")

    return df


def build_sparse_matrix(df):
    """
    Build a sparse item-user interaction matrix.

    Rows    = articles
    Columns = customers
    Values  = interaction strength
    """

    print("\nBuilding sparse item-user matrix...")

    # Convert IDs to integer indices.
    item_codes, item_ids = pd.factorize(df["article_id"])

    user_codes, user_ids = pd.factorize(df["customer_id"])

    # Interaction values.
    values = df["interaction_count"].astype(np.float32).to_numpy()

    matrix = csr_matrix(
        (
            values,
            (item_codes, user_codes)
        ),
        shape=(
            len(item_ids),
            len(user_ids)
        ),
        dtype=np.float32
    )

    print(f"Matrix shape: {matrix.shape}")
    print(f"Non-zero values: {matrix.nnz:,}")

    density = (
        matrix.nnz /
        (matrix.shape[0] * matrix.shape[1])
    )

    print(f"Matrix density: {density:.8%}")

    return matrix, item_ids, user_ids


def build_topk_similarity(matrix, item_ids):
    """
    Find only the TOP_K similar items for every item.

    This avoids constructing the full
    item x item similarity matrix.
    """

    print("\nCalculating top-K item similarity...")

    normalized_matrix = normalize(matrix, axis=1)

    model = NearestNeighbors(
        n_neighbors=TOP_K + 1,
        metric="cosine",
        algorithm="brute",
        n_jobs=-1
    )

    model.fit(normalized_matrix)

    distances, indices = model.kneighbors(
        normalized_matrix
    )

    print("Similarity calculation complete.")

    rows = []

    for item_index in range(len(item_ids)):

        for rank in range(1, TOP_K + 1):

            neighbor_index = indices[item_index, rank]

            distance = distances[item_index, rank]

            similarity = 1.0 - distance

            rows.append(
                (
                    int(item_ids[item_index]),
                    int(item_ids[neighbor_index]),
                    float(similarity),
                    rank
                )
            )

    similarity_df = pd.DataFrame(
        rows,
        columns=[
            "article_id",
            "similar_article_id",
            "similarity",
            "rank"
        ]
    )

    return similarity_df


def save_similarity(similarity_df):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    similarity_df.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print("\nSimilarity model saved:")
    print(OUTPUT_FILE)

    print(
        f"Rows saved: {len(similarity_df):,}"
    )


def show_example(similarity_df, df):

    popular_item = (
        df.groupby("article_id")[
            "interaction_count"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .index[0]
    )

    print("\nMost popular article:")
    print(popular_item)

    print("\nTop similar articles:")

    result = (
        similarity_df[
            similarity_df["article_id"] ==
            popular_item
        ]
        .sort_values("rank")
    )

    print(result.to_string(index=False))


def main():

    df = load_interactions()

    matrix, item_ids, user_ids = (
        build_sparse_matrix(df)
    )

    similarity_df = build_topk_similarity(
        matrix,
        item_ids
    )

    save_similarity(
        similarity_df
    )

    show_example(
        similarity_df,
        df
    )

    print("\nMODEL BUILD COMPLETE")


if __name__ == "__main__":
    main()