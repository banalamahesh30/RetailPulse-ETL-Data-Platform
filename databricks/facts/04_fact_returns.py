# Databricks notebook source
returns_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/returns.parquet"
)

display(returns_df)

# COMMAND ----------

returns_df.printSchema()

# COMMAND ----------

returns_df.count()

# COMMAND ----------

fact_returns_df = returns_df.select(
    "Return_ID",
    "Order_ID",
    "Delivery_Date",
    "Return_Date",
    "Return_Reason",
    "Refund_Amount",
    "Return_Status"
)

# COMMAND ----------

from pyspark.sql.functions import col

returns_df.groupBy("Return_ID") \
    .count() \
    .filter(col("count") > 1) \
    .count()

# COMMAND ----------

fact_returns_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/facts/fact_returns")