import os
import pandas as pd


INTERACTION_FILE = "data/features/interactions"
SIMILARITY_FILE = "data/models/item_similarity_topk.parquet"

TOP_N = 10


def load_data():
    print("Loading interaction data...")
    interactions = pd.read_parquet(INTERACTION_FILE)

    print("Loading item similarity model...")
    similarity = pd.read_parquet(SIMILARITY_FILE)

    print(f"Interactions: {len(interactions):,}")
    print(f"Similarity relationships: {len(similarity):,}")

    return interactions, similarity


def recommend_for_user(
    customer_id,
    interactions,
    similarity,
    top_n=TOP_N
):
    """
    Generate item recommendations for a customer
    using their historical interactions.
    """

    # Get user's history
    user_history = interactions[
        interactions["customer_id"] == customer_id
    ]

    if user_history.empty:
        return pd.DataFrame(
            columns=[
                "article_id",
                "score",
                "reason"
            ]
        )

    # Items already interacted with
    purchased_items = set(
        user_history["article_id"]
    )

    # Rank user's historical items
    user_history = (
        user_history
        .sort_values(
            "interaction_count",
            ascending=False
        )
    )

    candidates = []

    # Find similar items for each historical item
    for _, row in user_history.iterrows():

        item_id = row["article_id"]
        interaction_count = row["interaction_count"]

        similar_items = similarity[
            similarity["article_id"] == item_id
        ]

        for _, similar in similar_items.iterrows():

            candidate_id = similar[
                "similar_article_id"
            ]

            similarity_score = similar[
                "similarity"
            ]

            # Don't recommend something
            # the customer already interacted with.
            if candidate_id in purchased_items:
                continue

            # Combine similarity with
            # customer's interaction strength.
            score = (
                similarity_score *
                interaction_count
            )

            candidates.append(
                {
                    "article_id": candidate_id,
                    "score": score,
                    "reason": (
                        f"Similar to item "
                        f"{item_id}"
                    )
                }
            )

    if not candidates:
        return pd.DataFrame(
            columns=[
                "article_id",
                "score",
                "reason"
            ]
        )

    recommendations = pd.DataFrame(
        candidates
    )

    # Same item may be recommended
    # from multiple historical items.
    recommendations = (
        recommendations
        .groupby("article_id", as_index=False)
        .agg(
            score=("score", "sum"),
            reason=("reason", "first")
        )
    )

    # Highest score first
    recommendations = (
        recommendations
        .sort_values(
            "score",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )

    return recommendations


def find_test_user(interactions):
    """
    Find a user with enough interactions
    for a meaningful recommendation test.
    """

    user_counts = (
        interactions
        .groupby("customer_id")
        .size()
        .sort_values(
            ascending=False
        )
    )

    return user_counts.index[0]


def main():

    interactions, similarity = load_data()

    # Pick a user with multiple interactions
    customer_id = find_test_user(
        interactions
    )

    print("\nTest customer:")
    print(customer_id)

    history = interactions[
        interactions["customer_id"] ==
        customer_id
    ]

    print("\nCustomer history:")
    print(
        history[
            [
                "article_id",
                "interaction_count"
            ]
        ].to_string(index=False)
    )

    recommendations = recommend_for_user(
        customer_id,
        interactions,
        similarity,
        TOP_N
    )

    print("\nTop recommendations:")

    if recommendations.empty:
        print("No recommendations found.")
    else:
        print(
            recommendations.to_string(
                index=False
            )
        )

    print("\nRECOMMENDATION ENGINE COMPLETE")


if __name__ == "__main__":
    main()