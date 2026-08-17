# Databricks notebook source
sellers_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/sellers.parquet"
)

# COMMAND ----------

sellers_df.printSchema()

# COMMAND ----------

dim_seller_df = sellers_df.select(
    "Seller_ID",
    "Seller_Name",
    "Contact_Name",
    "Email",
    "Phone",
    "GST_Number",
    "City",
    "State",
    "Postal_Code",
    "Rating",
    "Registration_Date",
    "Seller_Status"
)

# COMMAND ----------

dim_seller_df.count()

# COMMAND ----------

from pyspark.sql.functions import col

dim_seller_df.groupBy("Seller_ID") \
    .count() \
    .filter(col("count") > 1) \
    .show()

# COMMAND ----------

dim_seller_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/dimensions/dim_seller")