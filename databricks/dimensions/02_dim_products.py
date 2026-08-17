# Databricks notebook source
products_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/products.parquet"
)

# COMMAND ----------

products_df.printSchema()

# COMMAND ----------

dim_product_df = products_df.select(
    "Product_ID",
    "Product_Name",
    "Brand",
    "Category",
    "Price",
    "Cost_Price",
    "Stock",
    "Weight",
    "Launch_Date",
    "Seller_ID",
    "Product_Status"
)

# COMMAND ----------

dim_product_df.count()

# COMMAND ----------

from pyspark.sql.functions import col

dim_product_df.groupBy("Product_ID") \
    .count() \
    .filter(col("count") > 1) \
    .show()

# COMMAND ----------

dim_product_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/dimensions/dim_product")