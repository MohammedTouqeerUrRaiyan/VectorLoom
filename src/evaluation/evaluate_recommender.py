"""
VectorLoom Recommendation Engine Evaluation

Time-based evaluation of the hybrid recommendation system.

Evaluation:
    Earlier interactions -> user history
    Latest interaction   -> ground truth

Metrics:
    Precision@K
    Recall@K
    Hit Rate@K

Uses:
    data/features/interactions/*.parquet
    data/models/item_similarity_topk.parquet
    data/models/content_similarity_topk.parquet

Output:
    data/evaluation/hybrid_evaluation_results.parquet
"""

from pathlib import Path
from collections import defaultdict
import random

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INTERACTIONS_PATH = (
    PROJECT_ROOT
    / "data"
    / "features"
    / "interactions"
)

COLLABORATIVE_MODEL_PATH = (
    PROJECT_ROOT
    / "data"
    / "models"
    / "item_similarity_topk.parquet"
)

CONTENT_MODEL_PATH = (
    PROJECT_ROOT
    / "data"
    / "models"
    / "content_similarity_topk.parquet"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "hybrid_evaluation_results.parquet"
)

K_VALUES = [5, 10, 20]

# Keep this manageable because we are working on a local machine.
MAX_EVALUATION_USERS = 1000

RANDOM_SEED = 42

# Hybrid weighting.
# Collaborative filtering gets higher weight because it represents
# actual user-item interaction behavior.
COLLABORATIVE_WEIGHT = 0.6
CONTENT_WEIGHT = 0.4


# ============================================================
# LOAD INTERACTIONS
# ============================================================

def load_interactions():

    print("=" * 60)
    print("VECTORLOOM RECOMMENDER EVALUATION")
    print("=" * 60)

    print("\nLoading interaction data...")

    files = sorted(
        INTERACTIONS_PATH.glob("part-*.parquet")
    )

    if not files:
        raise FileNotFoundError(
            f"No interaction parquet files found in {INTERACTIONS_PATH}"
        )

    print(f"Found {len(files)} interaction files.")

    frames = []

    for file in files:
        print(f"Loading: {file.name}")

        df_part = pd.read_parquet(file)

        # Only keep columns needed for evaluation.
        required_columns = [
            "customer_id",
            "article_id",
            "last_interaction_date",
            "interaction_count",
        ]

        df_part = df_part[required_columns]

        frames.append(df_part)

    df = pd.concat(
        frames,
        ignore_index=True
    )

    df["last_interaction_date"] = pd.to_datetime(
        df["last_interaction_date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "customer_id",
            "article_id",
            "last_interaction_date",
        ]
    )

    print(f"\nTotal interactions: {len(df):,}")
    print(
        f"Users: "
        f"{df['customer_id'].nunique():,}"
    )
    print(
        f"Items: "
        f"{df['article_id'].nunique():,}"
    )

    return df


# ============================================================
# LOAD SIMILARITY MODELS
# ============================================================

def load_similarity_models():

    print("\nLoading collaborative similarity model...")

    if not COLLABORATIVE_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Collaborative model not found:\n"
            f"{COLLABORATIVE_MODEL_PATH}"
        )

    collaborative = pd.read_parquet(
        COLLABORATIVE_MODEL_PATH
    )

    print(
        f"Collaborative relationships: "
        f"{len(collaborative):,}"
    )

    print("\nLoading content similarity model...")

    if not CONTENT_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Content model not found:\n"
            f"{CONTENT_MODEL_PATH}"
        )

    content = pd.read_parquet(
        CONTENT_MODEL_PATH
    )

    print(
        f"Content relationships: "
        f"{len(content):,}"
    )

    return collaborative, content


# ============================================================
# CREATE TIME-BASED SPLIT
# ============================================================

def create_test_split(df):

    print("\nCreating time-based evaluation split...")

    df = df.sort_values(
        [
            "customer_id",
            "last_interaction_date",
        ]
    ).copy()

    customer_counts = (
        df.groupby("customer_id")
        .size()
    )

    eligible_users = customer_counts[
        customer_counts >= 2
    ].index

    df = df[
        df["customer_id"].isin(
            eligible_users
        )
    ].copy()

    # Latest interaction = test interaction.
    test = (
        df.groupby("customer_id")
        .tail(1)
        .copy()
    )

    # Everything before latest interaction = training history.
    test_indices = test.index

    train = df.drop(
        index=test_indices
    ).copy()

    print(
        f"Eligible users: "
        f"{len(eligible_users):,}"
    )

    print(
        f"Training interactions: "
        f"{len(train):,}"
    )

    print(
        f"Test interactions: "
        f"{len(test):,}"
    )

    return train, test


# ============================================================
# SAMPLE USERS
# ============================================================

def sample_evaluation_users(
    train,
    test
):

    print(
        "\nSelecting evaluation users..."
    )

    eligible_users = (
        test["customer_id"]
        .unique()
        .tolist()
    )

    random.seed(
        RANDOM_SEED
    )

    if len(eligible_users) > MAX_EVALUATION_USERS:

        selected_users = random.sample(
            eligible_users,
            MAX_EVALUATION_USERS
        )

    else:

        selected_users = eligible_users

    print(
        f"Users selected for evaluation: "
        f"{len(selected_users):,}"
    )

    return selected_users


# ============================================================
# BUILD USER HISTORY
# ============================================================

def build_user_history(
    train,
    selected_users
):

    print(
        "\nBuilding user histories..."
    )

    train = train[
        train["customer_id"].isin(
            selected_users
        )
    ]

    history = defaultdict(
        list
    )

    for row in train.itertuples(
        index=False
    ):

        history[row.customer_id].append(
            (
                int(row.article_id),
                float(row.interaction_count)
            )
        )

    print(
        f"Users with training history: "
        f"{len(history):,}"
    )

    return history


# ============================================================
# BUILD GROUND TRUTH
# ============================================================

def build_ground_truth(
    test,
    selected_users
):

    test = test[
        test["customer_id"].isin(
            selected_users
        )
    ]

    ground_truth = {}

    for row in test.itertuples(
        index=False
    ):

        ground_truth[
            row.customer_id
        ] = {
            int(row.article_id)
        }

    print(
        f"Ground-truth users: "
        f"{len(ground_truth):,}"
    )

    return ground_truth


# ============================================================
# PREPARE SIMILARITY MAP
# ============================================================

def build_similarity_map(
    df,
    name
):

    print(
        f"\nPreparing {name} similarity map..."
    )

    similarity_map = defaultdict(
        list
    )

    for row in df.itertuples(
        index=False
    ):

        article_id = int(
            row.article_id
        )

        similar_article_id = int(
            row.similar_article_id
        )

        similarity = float(
            row.similarity
        )

        similarity_map[
            article_id
        ].append(
            (
                similar_article_id,
                similarity
            )
        )

    print(
        f"{name} source articles: "
        f"{len(similarity_map):,}"
    )

    return similarity_map


# ============================================================
# GENERATE RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    user_history,
    collaborative_map,
    content_map,
    top_k=20
):

    scores = defaultdict(
        lambda: {
            "collaborative": 0.0,
            "content": 0.0,
        }
    )

    history_items = {
        article_id
        for article_id, _ in user_history
    }

    # --------------------------------------------------------
    # Collaborative recommendations
    # --------------------------------------------------------

    for article_id, interaction_count in user_history:

        similar_items = collaborative_map.get(
            article_id,
            []
        )

        for similar_article, similarity in similar_items:

            if similar_article in history_items:
                continue

            scores[
                similar_article
            ]["collaborative"] += (
                similarity
                * interaction_count
            )

    # --------------------------------------------------------
    # Content recommendations
    # --------------------------------------------------------

    for article_id, interaction_count in user_history:

        similar_items = content_map.get(
            article_id,
            []
        )

        for similar_article, similarity in similar_items:

            if similar_article in history_items:
                continue

            scores[
                similar_article
            ]["content"] += (
                similarity
                * interaction_count
            )

    # --------------------------------------------------------
    # Combine scores
    # --------------------------------------------------------

    final_scores = []

    for article_id, values in scores.items():

        collaborative_score = (
            values["collaborative"]
        )

        content_score = (
            values["content"]
        )

        hybrid_score = (
            COLLABORATIVE_WEIGHT
            * collaborative_score
            +
            CONTENT_WEIGHT
            * content_score
        )

        final_scores.append(
            (
                article_id,
                hybrid_score
            )
        )

    final_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return [
        article_id
        for article_id, score
        in final_scores[:top_k]
    ]


# ============================================================
# PRECISION@K
# ============================================================

def precision_at_k(
    recommended,
    relevant,
    k
):

    recommended_k = recommended[:k]

    if not recommended_k:
        return 0.0

    hits = len(
        set(recommended_k)
        &
        relevant
    )

    return hits / len(
        recommended_k
    )


# ============================================================
# RECALL@K
# ============================================================

def recall_at_k(
    recommended,
    relevant,
    k
):

    if not relevant:
        return 0.0

    recommended_k = recommended[:k]

    hits = len(
        set(recommended_k)
        &
        relevant
    )

    return hits / len(
        relevant
    )


# ============================================================
# HIT RATE@K
# ============================================================

def hit_rate_at_k(
    recommended,
    relevant,
    k
):

    recommended_k = recommended[:k]

    hits = (
        set(recommended_k)
        &
        relevant
    )

    return (
        1.0
        if hits
        else 0.0
    )


# ============================================================
# EVALUATION
# ============================================================

def evaluate_model(
    user_history,
    ground_truth,
    collaborative_map,
    content_map
):

    print(
        "\n" + "=" * 60
    )

    print(
        "CALCULATING METRICS"
    )

    print(
        "=" * 60
    )

    results = []

    total_users = len(
        ground_truth
    )

    for counter, (
        customer_id,
        relevant_items
    ) in enumerate(
        ground_truth.items(),
        start=1
    ):

        history = user_history.get(
            customer_id,
            []
        )

        if not history:
            continue

        recommendations = generate_recommendations(
            history,
            collaborative_map,
            content_map,
            top_k=max(K_VALUES)
        )

        row = {
            "customer_id": customer_id,
            "history_size": len(history),
            "ground_truth_size": len(
                relevant_items
            ),
        }

        for k in K_VALUES:

            row[
                f"precision@{k}"
            ] = precision_at_k(
                recommendations,
                relevant_items,
                k
            )

            row[
                f"recall@{k}"
            ] = recall_at_k(
                recommendations,
                relevant_items,
                k
            )

            row[
                f"hit_rate@{k}"
            ] = hit_rate_at_k(
                recommendations,
                relevant_items,
                k
            )

        results.append(row)

        if (
            counter % 100 == 0
            or counter == total_users
        ):

            print(
                f"Evaluated: "
                f"{counter:,}/"
                f"{total_users:,}"
            )

    return pd.DataFrame(
        results
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(
    results
):

    print(
        "\n" + "=" * 60
    )

    print(
        "VECTORLOOM MODEL EVALUATION RESULTS"
    )

    print(
        "=" * 60
    )

    print(
        f"\nUsers evaluated: "
        f"{len(results):,}"
    )

    for k in K_VALUES:

        precision = results[
            f"precision@{k}"
        ].mean()

        recall = results[
            f"recall@{k}"
        ].mean()

        hit_rate = results[
            f"hit_rate@{k}"
        ].mean()

        print(
            f"\nK = {k}"
        )

        print(
            "-" * 40
        )

        print(
            f"Precision@{k}: "
            f"{precision:.4f}"
        )

        print(
            f"Recall@{k}:    "
            f"{recall:.4f}"
        )

        print(
            f"Hit Rate@{k}:  "
            f"{hit_rate:.4f}"
        )


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(
    results
):

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    results.to_parquet(
        OUTPUT_PATH,
        index=False
    )

    print(
        "\nEvaluation results saved:"
    )

    print(
        OUTPUT_PATH
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # 1. Load interaction data
    interactions = load_interactions()

    # 2. Load similarity models
    collaborative, content = (
        load_similarity_models()
    )

    # 3. Time-based split
    train, test = create_test_split(
        interactions
    )

    # 4. Select manageable evaluation sample
    selected_users = sample_evaluation_users(
        train,
        test
    )

    # 5. Build user history
    user_history = build_user_history(
        train,
        selected_users
    )

    # 6. Build ground truth
    ground_truth = build_ground_truth(
        test,
        selected_users
    )

    # 7. Build similarity lookup maps
    collaborative_map = build_similarity_map(
        collaborative,
        "collaborative"
    )

    content_map = build_similarity_map(
        content,
        "content"
    )

    # 8. Evaluate
    results = evaluate_model(
        user_history,
        ground_truth,
        collaborative_map,
        content_map
    )

    if results.empty:

        raise RuntimeError(
            "No users were successfully evaluated."
        )

    # 9. Display metrics
    display_results(
        results
    )

    # 10. Save
    save_results(
        results
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "EVALUATION COMPLETE"
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":
    main()