from pathlib import Path
from typing import Optional

import pandas as pd


class RecommendationService:
    """
    Runtime recommendation service for VectorLoom.

    Loads precomputed hybrid recommendations from disk and
    provides recommendations for individual customers.

    Offline model building happens in:
        src/models/

    Runtime recommendation serving happens here:
        src/recommendation/
    """

    _recommendations: Optional[pd.DataFrame] = None
    _articles: Optional[pd.DataFrame] = None

    MODEL_PATH = Path(
        "data/models/hybrid_recommendations.parquet"
    )

    ARTICLES_PATH = Path(
        "data/hm/articles.parquet"
    )

    @classmethod
    def load_model(cls) -> pd.DataFrame:
        """
        Load the precomputed hybrid recommendation model.

        The model is loaded only once and cached in memory.
        """

        if cls._recommendations is not None:
            return cls._recommendations

        if not cls.MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Recommendation model not found: "
                f"{cls.MODEL_PATH}"
            )

        df = pd.read_parquet(cls.MODEL_PATH)

        required_columns = {
            "customer_id",
            "article_id",
            "hybrid_score",
        }

        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(
                "Recommendation model is missing required "
                f"columns: {sorted(missing_columns)}"
            )

        df["customer_id"] = (
            df["customer_id"].astype(str)
        )

        df["article_id"] = (
            df["article_id"].astype(str)
        )

        cls._recommendations = df

        return cls._recommendations

    @classmethod
    def load_articles(cls) -> pd.DataFrame:
        """
        Load H&M article metadata.

        The article metadata is loaded only once and
        cached in memory.
        """

        if cls._articles is not None:
            return cls._articles

        if not cls.ARTICLES_PATH.exists():
            raise FileNotFoundError(
                f"Articles dataset not found: "
                f"{cls.ARTICLES_PATH}"
            )

        df = pd.read_parquet(
            cls.ARTICLES_PATH
        )

        required_columns = {
            "article_id",
            "prod_name",
            "product_type_name",
            "product_group_name",
            "colour_group_name",
            "department_name",
            "section_name",
            "detail_desc",
        }

        missing_columns = (
            required_columns - set(df.columns)
        )

        if missing_columns:
            raise ValueError(
                "Articles dataset is missing required "
                f"columns: {sorted(missing_columns)}"
            )

        df["article_id"] = (
            df["article_id"].astype(str)
        )

        cls._articles = df

        return cls._articles

    @classmethod
    def get_recommendations(
        cls,
        customer_id: str,
        limit: int = 10,
    ) -> list[dict]:
        """
        Return enriched recommendations for a customer.
        """

        if not customer_id:
            raise ValueError(
                "customer_id cannot be empty."
            )

        if limit <= 0:
            raise ValueError(
                "limit must be greater than zero."
            )

        recommendations = cls.load_model()

        user_recommendations = recommendations[
            recommendations["customer_id"]
            == str(customer_id)
        ]

        if user_recommendations.empty:
            return []

        user_recommendations = (
            user_recommendations
            .sort_values(
                "hybrid_score",
                ascending=False,
            )
            .head(limit)
        )

        # --------------------------------------------------
        # Load article metadata
        # --------------------------------------------------

        articles = cls.load_articles()

        # --------------------------------------------------
        # Create lookup table for recommended articles
        # --------------------------------------------------

        article_ids = (
            user_recommendations["article_id"]
            .astype(str)
            .tolist()
        )

        article_metadata = articles[
            articles["article_id"].isin(article_ids)
        ]

        article_metadata = (
            article_metadata
            .drop_duplicates(
                subset=["article_id"]
            )
            .set_index("article_id")
        )

        # --------------------------------------------------
        # Build API response
        # --------------------------------------------------

        results = []

        for _, row in user_recommendations.iterrows():

            article_id = str(
                row["article_id"]
            )

            metadata = (
                article_metadata.loc[article_id]
                if article_id in article_metadata.index
                else None
            )

            result = {
                "article_id": article_id,

                "product_name": (
                    str(metadata["prod_name"])
                    if metadata is not None
                    else None
                ),

                "product_type": (
                    str(metadata["product_type_name"])
                    if metadata is not None
                    else None
                ),

                "product_group": (
                    str(metadata["product_group_name"])
                    if metadata is not None
                    else None
                ),

                "colour": (
                    str(metadata["colour_group_name"])
                    if metadata is not None
                    else None
                ),

                "department": (
                    str(metadata["department_name"])
                    if metadata is not None
                    else None
                ),

                "section": (
                    str(metadata["section_name"])
                    if metadata is not None
                    else None
                ),

                "description": (
                    str(metadata["detail_desc"])
                    if metadata is not None
                    else None
                ),

                "score": float(
                    row["hybrid_score"]
                ),
            }

            if "collaborative_score" in row:
                result["collaborative_score"] = float(
                    row["collaborative_score"]
                )

            if "content_score" in row:
                result["content_score"] = float(
                    row["content_score"]
                )

            if "reason" in row:
                result["reason"] = str(
                    row["reason"]
                )

            results.append(result)

        return results

    @classmethod
    def has_customer(
        cls,
        customer_id: str,
    ) -> bool:
        """
        Check whether recommendations exist
        for a customer.
        """

        recommendations = cls.load_model()

        return (
            recommendations["customer_id"]
            .eq(str(customer_id))
            .any()
        )

    @classmethod
    def get_customer_count(cls) -> int:
        """
        Return the number of customers available
        in the recommendation model.
        """

        recommendations = cls.load_model()

        return int(
            recommendations["customer_id"]
            .nunique()
        )

    @classmethod
    def reload_model(cls) -> None:
        """
        Clear the cached recommendation and article data.

        Useful after rebuilding:
            hybrid_recommendations.parquet
            articles.parquet
        """

        cls._recommendations = None
        cls._articles = None