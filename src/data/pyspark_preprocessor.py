# src/data/pyspark_preprocessor.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def init_spark():
    """Initializes local Spark Session optimized for VectorLoom data handling."""
    spark = SparkSession.builder \
        .appName("VectorLoom-DataPrep") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()
    return spark

def clean_transaction_data(df):
    """
    Handles missing values and cleans up the transaction history baseline.
    Address Cold-start strategy: fills sparse features or flags missing values.
    """
    cleaned_df = df.filter(col("customer_id").isNotNull()) \
                   .withColumn("price", col("price").cast("float"))
    return cleaned_df

if __name__ == "__main__":
    spark = init_spark()
    print("VectorLoom Spark Session successfully initialized.")