from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

ARTICLES_PATH = Path("data/hm/articles.parquet")
MODEL_DIR = Path("data/models")
OUTPUT_PATH = MODEL_DIR / "content_similarity_topk.parquet"

TOP_K = 20

# Process this many articles at a time.
# Lower this if memory is still tight.
BATCH_SIZE = 1000


# ---------------------------------------------------------
# Load articles
# ---------------------------------------------------------

def load_articles():

    print("Loading article metadata...")

    df = pd.read_parquet(ARTICLES_PATH)

    print(f"Articles loaded: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    return df


# ---------------------------------------------------------
# Build content text
# ---------------------------------------------------------

def build_text_features(df):

    print("\nBuilding content representation...")

    text_columns = [
        "prod_name",
        "product_type_name",
        "product_group_name",
        "graphical_appearance_name",
        "colour_group_name",
        "perceived_colour_value_name",
        "perceived_colour_master_name",
        "department_name",
        "index_name",
        "index_group_name",
        "section_name",
        "garment_group_name",
        "detail_desc",
    ]

    available_columns = [
        column
        for column in text_columns
        if column in df.columns
    ]

    print("Using columns:")

    for column in available_columns:
        print(f"  - {column}")

    text_df = df[available_columns].fillna("")

    df = df.copy()

    df["content_text"] = text_df.astype(str).agg(
        " ".join,
        axis=1
    )

    return df


# ---------------------------------------------------------
# TF-IDF
# ---------------------------------------------------------

def create_tfidf(df):

    print("\nCreating TF-IDF representation...")

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        max_features=100_000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
    )

    matrix = vectorizer.fit_transform(
        df["content_text"]
    )

    print(f"TF-IDF matrix shape: {matrix.shape}")
    print(f"Non-zero values: {matrix.nnz:,}")

    return matrix


# ---------------------------------------------------------
# Batch similarity calculation
# ---------------------------------------------------------

def calculate_similarity(matrix, article_ids):

    print("\nCalculating content similarity in batches...")

    n_items = matrix.shape[0]

    print(f"Total articles: {n_items:,}")
    print(f"Batch size: {BATCH_SIZE:,}")
    print(f"Top-K: {TOP_K}")

    # Fit the nearest-neighbor index ONCE.
    #
    # The index stores the sparse TF-IDF matrix.
    # We then query it batch-by-batch.
    model = NearestNeighbors(
        n_neighbors=TOP_K + 1,
        metric="cosine",
        algorithm="brute",
        n_jobs=1,
    )

    model.fit(matrix)

    all_rows = []

    for start in range(0, n_items, BATCH_SIZE):

        end = min(
            start + BATCH_SIZE,
            n_items
        )

        print(
            f"Processing articles "
            f"{start:,} - {end:,} "
            f"of {n_items:,}"
        )

        batch = matrix[start:end]

        distances, indices = model.kneighbors(
            batch,
            return_distance=True,
        )

        for local_index in range(
            end - start
        ):

            source_index = start + local_index

            source_article = article_ids[
                source_index
            ]

            for rank in range(
                1,
                TOP_K + 1
            ):

                neighbor_index = indices[
                    local_index,
                    rank
                ]

                distance = distances[
                    local_index,
                    rank
                ]

                similarity = 1.0 - distance

                similar_article = article_ids[
                    neighbor_index
                ]

                all_rows.append(
                    {
                        "article_id": int(
                            source_article
                        ),
                        "similar_article_id": int(
                            similar_article
                        ),
                        "similarity": float(
                            similarity
                        ),
                        "rank": rank,
                    }
                )

        # Progress
        processed = end

        print(
            f"Completed: "
            f"{processed:,}/{n_items:,} "
            f"({processed / n_items * 100:.1f}%)"
        )

    return pd.DataFrame(all_rows)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("VECTORLOOM CONTENT-BASED SIMILARITY MODEL")
    print("=" * 60)

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------------------
    # 1. Load articles
    # -----------------------------------------------------

    articles = load_articles()

    # -----------------------------------------------------
    # 2. Build content representation
    # -----------------------------------------------------

    articles = build_text_features(
        articles
    )

    # -----------------------------------------------------
    # 3. TF-IDF
    # -----------------------------------------------------

    tfidf_matrix = create_tfidf(
        articles
    )

    # -----------------------------------------------------
    # 4. Similarity
    # -----------------------------------------------------

    article_ids = articles[
        "article_id"
    ].tolist()

    similarity_df = calculate_similarity(
        tfidf_matrix,
        article_ids
    )

    # -----------------------------------------------------
    # 5. Save
    # -----------------------------------------------------

    similarity_df.to_parquet(
        OUTPUT_PATH,
        index=False
    )

    # -----------------------------------------------------
    # 6. Report
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("CONTENT MODEL BUILD COMPLETE")
    print("=" * 60)

    print(
        f"Rows saved: "
        f"{len(similarity_df):,}"
    )

    print(
        f"Output: "
        f"{OUTPUT_PATH}"
    )

    print("\nSimilarity statistics:")

    print(
        similarity_df[
            "similarity"
        ].describe()
    )

    # -----------------------------------------------------
    # Example
    # -----------------------------------------------------

    example_article = article_ids[0]

    print(
        f"\nExample article: "
        f"{example_article}"
    )

    print("\nTop similar articles:")

    example = (
        similarity_df[
            similarity_df["article_id"]
            == example_article
        ]
        .head(10)
    )

    print(
        example.to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()