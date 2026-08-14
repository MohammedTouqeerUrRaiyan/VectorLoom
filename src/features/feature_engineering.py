from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def create_spark():

    return (
        SparkSession.builder
        .appName("VectorLoom-FeatureEngineering")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )


def build_features():

    spark = create_spark()

    transactions_path = "data/hm/transactions_sample.parquet"
    articles_path = "data/hm/articles.parquet"

    transactions = spark.read.parquet(transactions_path)
    articles = spark.read.parquet(articles_path)

    print("Transactions:", transactions.count())
    print("Articles:", articles.count())

    # --------------------------------------------------
    # Basic cleaning
    # --------------------------------------------------

    transactions = (
        transactions
        .dropna(subset=["customer_id", "article_id", "t_dat"])
        .withColumn("t_dat", F.to_date("t_dat"))
        .withColumn("price", F.col("price").cast("double"))
        .withColumn(
            "article_id",
            F.col("article_id").cast("long")
        )
    )

    # --------------------------------------------------
    # Contextual time features
    # --------------------------------------------------

    transactions = (
        transactions
        .withColumn("year", F.year("t_dat"))
        .withColumn("month", F.month("t_dat"))
        .withColumn("day_of_week", F.dayofweek("t_dat"))
        .withColumn("week_of_year", F.weekofyear("t_dat"))
    )

    # --------------------------------------------------
    # Global reference date
    # --------------------------------------------------

    reference_date = transactions.select(
        F.max("t_dat").alias("max_date")
    ).collect()[0]["max_date"]

    print("Reference date:", reference_date)

    # --------------------------------------------------
    # USER FEATURES
    # --------------------------------------------------

    user_features = (
        transactions
        .groupBy("customer_id")
        .agg(
            F.count("*").alias("purchase_count"),

            F.countDistinct("article_id")
            .alias("unique_items"),

            F.avg("price")
            .alias("avg_price"),

            F.max("t_dat")
            .alias("last_purchase_date"),

            F.min("t_dat")
            .alias("first_purchase_date"),
        )
        .withColumn(
            "recency_days",
            F.datediff(
                F.lit(reference_date),
                F.col("last_purchase_date")
            )
        )
        .withColumn(
            "customer_lifetime_days",
            F.datediff(
                F.col("last_purchase_date"),
                F.col("first_purchase_date")
            )
        )
    )

    # --------------------------------------------------
    # ITEM FEATURES
    # --------------------------------------------------

    item_features = (
        transactions
        .groupBy("article_id")
        .agg(
            F.count("*").alias("purchase_count"),

            F.countDistinct("customer_id")
            .alias("unique_customers"),

            F.avg("price")
            .alias("avg_price"),

            F.max("t_dat")
            .alias("last_purchase_date"),
        )
        .withColumn(
            "item_recency_days",
            F.datediff(
                F.lit(reference_date),
                F.col("last_purchase_date")
            )
        )
    )

    # --------------------------------------------------
    # POPULARITY
    # --------------------------------------------------

    popularity_window = Window.orderBy(
        F.desc("purchase_count")
    )

    item_features = (
        item_features
        .withColumn(
            "popularity_rank",
            F.row_number().over(popularity_window)
        )
    )

    # --------------------------------------------------
    # USER-ITEM INTERACTIONS
    # --------------------------------------------------

    interactions = (
        transactions
        .groupBy(
            "customer_id",
            "article_id"
        )
        .agg(
            F.count("*").alias("interaction_count"),

            F.max("t_dat")
            .alias("last_interaction_date"),

            F.avg("price")
            .alias("interaction_avg_price")
        )
    )

    # --------------------------------------------------
    # JOIN ARTICLE CONTEXT
    # --------------------------------------------------

    article_context = articles.select(
        "article_id",
        *[
            c for c in articles.columns
            if c != "article_id"
        ]
    )

    interactions = interactions.join(
        article_context,
        on="article_id",
        how="left"
    )

    # --------------------------------------------------
    # SAVE FEATURES
    # --------------------------------------------------

    output_dir = "data/features"

    user_features.write.mode("overwrite").parquet(
        f"{output_dir}/users"
    )

    item_features.write.mode("overwrite").parquet(
        f"{output_dir}/items"
    )

    interactions.write.mode("overwrite").parquet(
        f"{output_dir}/interactions"
    )

    print()
    print("FEATURE ENGINEERING COMPLETE")
    print(
        "Users:",
        user_features.count()
    )
    print(
        "Items:",
        item_features.count()
    )
    print(
        "Interactions:",
        interactions.count()
    )

    spark.stop()


if __name__ == "__main__":
    build_features()