from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

INTERACTIONS_PATH = Path(
    "data/features/interactions"
)

COLLAB_MODEL_PATH = Path(
    "data/models/item_similarity_topk.parquet"
)

CONTENT_MODEL_PATH = Path(
    "data/models/content_similarity_topk.parquet"
)

OUTPUT_PATH = Path(
    "data/models/hybrid_recommendations.parquet"
)

TOP_N = 10

# Weight given to collaborative filtering.
COLLAB_WEIGHT = 0.70

# Weight given to content-based filtering.
CONTENT_WEIGHT = 0.30


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("=" * 60)
    print("VECTORLOOM HYBRID RECOMMENDER")
    print("=" * 60)

    print("\nLoading interaction data...")

    interactions = pd.read_parquet(
        INTERACTIONS_PATH
    )

    print(
        f"Interactions: "
        f"{len(interactions):,}"
    )

    print("\nLoading collaborative model...")

    collaborative = pd.read_parquet(
        COLLAB_MODEL_PATH
    )

    print(
        f"Collaborative relationships: "
        f"{len(collaborative):,}"
    )

    print("\nLoading content model...")

    content = pd.read_parquet(
        CONTENT_MODEL_PATH
    )

    print(
        f"Content relationships: "
        f"{len(content):,}"
    )

    return (
        interactions,
        collaborative,
        content,
    )


# ============================================================
# USER HISTORY
# ============================================================

def get_user_history(
    interactions,
    customer_id,
):

    history = (
        interactions[
            interactions["customer_id"]
            == customer_id
        ]
        .groupby("article_id")[
            "interaction_count"
        ]
        .sum()
        .reset_index()
    )

    return history


# ============================================================
# COLLABORATIVE CANDIDATES
# ============================================================

def get_collaborative_candidates(
    history,
    collaborative,
):

    if history.empty:
        return pd.DataFrame(
            columns=[
                "article_id",
                "collaborative_score",
            ]
        )

    history_ids = set(
        history["article_id"]
    )

    candidates = collaborative[
        collaborative["article_id"].isin(
            history_ids
        )
    ].copy()

    if candidates.empty:
        return pd.DataFrame(
            columns=[
                "article_id",
                "collaborative_score",
            ]
        )

    # Weight similarity by user's interaction count.
    history_weights = (
        history
        .set_index("article_id")[
            "interaction_count"
        ]
        .to_dict()
    )

    candidates["interaction_weight"] = (
        candidates["article_id"]
        .map(history_weights)
        .fillna(1)
    )

    candidates["weighted_score"] = (
        candidates["similarity"]
        * candidates["interaction_weight"]
    )

    candidates = (
        candidates
        .groupby("similar_article_id")[
            "weighted_score"
        ]
        .sum()
        .reset_index()
    )

    candidates = candidates.rename(
        columns={
            "similar_article_id":
                "article_id",
            "weighted_score":
                "collaborative_score",
        }
    )

    return candidates


# ============================================================
# CONTENT CANDIDATES
# ============================================================

def get_content_candidates(
    history,
    content,
):

    if history.empty:
        return pd.DataFrame(
            columns=[
                "article_id",
                "content_score",
            ]
        )

    history_ids = set(
        history["article_id"]
    )

    candidates = content[
        content["article_id"].isin(
            history_ids
        )
    ].copy()

    if candidates.empty:
        return pd.DataFrame(
            columns=[
                "article_id",
                "content_score",
            ]
        )

    history_weights = (
        history
        .set_index("article_id")[
            "interaction_count"
        ]
        .to_dict()
    )

    candidates["interaction_weight"] = (
        candidates["article_id"]
        .map(history_weights)
        .fillna(1)
    )

    candidates["weighted_score"] = (
        candidates["similarity"]
        * candidates["interaction_weight"]
    )

    candidates = (
        candidates
        .groupby("similar_article_id")[
            "weighted_score"
        ]
        .sum()
        .reset_index()
    )

    candidates = candidates.rename(
        columns={
            "similar_article_id":
                "article_id",
            "weighted_score":
                "content_score",
        }
    )

    return candidates


# ============================================================
# HYBRID SCORING
# ============================================================

def calculate_hybrid_scores(
    collaborative_candidates,
    content_candidates,
):

    hybrid = pd.merge(
        collaborative_candidates,
        content_candidates,
        on="article_id",
        how="outer",
    )

    hybrid[
        "collaborative_score"
    ] = hybrid[
        "collaborative_score"
    ].fillna(0)

    hybrid[
        "content_score"
    ] = hybrid[
        "content_score"
    ].fillna(0)

    # Normalize each component separately.
    #
    # This is important because the two models
    # may produce scores on different scales.

    coll_max = hybrid[
        "collaborative_score"
    ].max()

    content_max = hybrid[
        "content_score"
    ].max()

    if coll_max > 0:

        hybrid[
            "collaborative_normalized"
        ] = (
            hybrid["collaborative_score"]
            / coll_max
        )

    else:

        hybrid[
            "collaborative_normalized"
        ] = 0.0

    if content_max > 0:

        hybrid[
            "content_normalized"
        ] = (
            hybrid["content_score"]
            / content_max
        )

    else:

        hybrid[
            "content_normalized"
        ] = 0.0

    # Final hybrid score.

    hybrid["hybrid_score"] = (
        COLLAB_WEIGHT
        * hybrid[
            "collaborative_normalized"
        ]
        +
        CONTENT_WEIGHT
        * hybrid[
            "content_normalized"
        ]
    )

    hybrid = hybrid.sort_values(
        "hybrid_score",
        ascending=False,
    )

    return hybrid


# ============================================================
# REMOVE SEEN ITEMS
# ============================================================

def remove_seen_items(
    recommendations,
    history,
):

    seen_items = set(
        history["article_id"]
    )

    recommendations = (
        recommendations[
            ~recommendations[
                "article_id"
            ].isin(seen_items)
        ]
        .copy()
    )

    return recommendations


# ============================================================
# RECOMMEND
# ============================================================

def recommend(
    customer_id,
    interactions,
    collaborative,
    content,
    top_n=TOP_N,
):

    print("\n" + "-" * 60)

    print(
        f"Generating recommendations for:"
        f"\n{customer_id}"
    )

    history = get_user_history(
        interactions,
        customer_id,
    )

    print(
        f"\nUser history items: "
        f"{len(history)}"
    )

    if history.empty:

        print(
            "No interaction history found."
        )

        return pd.DataFrame()

    collaborative_candidates = (
        get_collaborative_candidates(
            history,
            collaborative,
        )
    )

    content_candidates = (
        get_content_candidates(
            history,
            content,
        )
    )

    print(
        f"Collaborative candidates: "
        f"{len(collaborative_candidates):,}"
    )

    print(
        f"Content candidates: "
        f"{len(content_candidates):,}"
    )

    hybrid = calculate_hybrid_scores(
        collaborative_candidates,
        content_candidates,
    )

    hybrid = remove_seen_items(
        hybrid,
        history,
    )

    hybrid = hybrid.head(
        top_n
    ).copy()

    hybrid["customer_id"] = customer_id

    hybrid["reason"] = hybrid.apply(
        lambda row:
            (
                "Collaborative + Content"
                if (
                    row[
                        "collaborative_score"
                    ] > 0
                    and
                    row[
                        "content_score"
                    ] > 0
                )
                else
                (
                    "Collaborative"
                    if row[
                        "collaborative_score"
                    ] > 0
                    else
                    "Content"
                )
            ),
        axis=1,
    )

    return hybrid[
        [
            "customer_id",
            "article_id",
            "hybrid_score",
            "collaborative_score",
            "content_score",
            "reason",
        ]
    ]


# ============================================================
# MAIN
# ============================================================

def main():

    (
        interactions,
        collaborative,
        content,
    ) = load_data()

    # --------------------------------------------------------
    # Use the same test customer we used earlier.
    # --------------------------------------------------------

    test_customer = (
        "75c54a755b8a467e53e0a4e01833deb029734feb22ad25438137925123a38f8b"
    )

    recommendations = recommend(
        customer_id=test_customer,
        interactions=interactions,
        collaborative=collaborative,
        content=content,
        top_n=TOP_N,
    )

    if recommendations.empty:

        print(
            "\nNo recommendations generated."
        )

        return

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("TOP HYBRID RECOMMENDATIONS")
    print("=" * 60)

    print(
        recommendations.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    recommendations.to_parquet(
        OUTPUT_PATH,
        index=False,
    )

    print(
        "\nRecommendations saved:"
    )

    print(
        OUTPUT_PATH
    )

    print(
        "\nHYBRID RECOMMENDER COMPLETE"
    )


if __name__ == "__main__":
    main()