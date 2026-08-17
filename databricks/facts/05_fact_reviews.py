# Databricks notebook source
reviews_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/reviews.parquet"
)

# COMMAND ----------

reviews_df.printSchema()

# COMMAND ----------

reviews_df.count()

# COMMAND ----------

from pyspark.sql.functions import col
from pyspark.sql.types import LongType, IntegerType

reviews_df = reviews_df \
    .withColumn("Review_ID", col("Review_ID").cast(LongType())) \
    .withColumn("Customer_ID", col("Customer_ID").cast(LongType())) \
    .withColumn("Product_ID", col("Product_ID").cast(LongType())) \
    .withColumn("Rating", col("Rating").cast(IntegerType())) \
    .withColumn("Review_Date", col("Review_Date").cast("date"))

# COMMAND ----------

reviews_df.printSchema()

# COMMAND ----------

fact_reviews_df = reviews_df.select(
    "Review_ID",
    "Customer_ID",
    "Product_ID",
    "Rating",
    "Review_Date",
    "Review_Text"
)

# COMMAND ----------

fact_reviews_df.count()

# COMMAND ----------

dim_customer = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/dimensions/dim_customer"
)

dim_product = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/dimensions/dim_product"
)

# COMMAND ----------

invalid_customer = fact_reviews_df.join(
    dim_customer.select("Customer_ID"),
    on="Customer_ID",
    how="left_anti"
)

invalid_customer.count()

# COMMAND ----------

fact_reviews_df.printSchema()
dim_customer.printSchema()

# COMMAND ----------

invalid_customer.select("Customer_ID").distinct().show(20, truncate=False)

# COMMAND ----------

from pyspark.sql.functions import col

fact_reviews_df = fact_reviews_df.filter(
    ~col("Customer_ID").isin(-1, 888888, 999999)
)

# COMMAND ----------

invalid_customer = fact_reviews_df.join(
    dim_customer.select("Customer_ID"),
    on="Customer_ID",
    how="left_anti"
)

invalid_customer.count()

# COMMAND ----------

invalid_product = fact_reviews_df.join(
    dim_product.select("Product_ID"),
    on="Product_ID",
    how="left_anti"
)

invalid_product.count()

# COMMAND ----------

invalid_product.select("Product_ID").distinct().show(20, truncate=False)

# COMMAND ----------

from pyspark.sql.functions import col

fact_reviews_df = fact_reviews_df.filter(
    ~col("Product_ID").isin(-5, 888888, 999999)
)

# COMMAND ----------

invalid_product = fact_reviews_df.join(
    dim_product.select("Product_ID"),
    on="Product_ID",
    how="left_anti"
)

invalid_product.count()

# COMMAND ----------

invalid_customer = fact_reviews_df.join(
    dim_customer.select("Customer_ID"),
    on="Customer_ID",
    how="left_anti"
)

invalid_customer.count()

# COMMAND ----------

fact_reviews_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/facts/fact_reviews")

fact_reviews_df.count()