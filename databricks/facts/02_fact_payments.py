# Databricks notebook source
payments_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/payments.parquet"
)

# COMMAND ----------

payments_df.printSchema()

# COMMAND ----------

fact_payments_df = payments_df.select(
    "Payment_ID",
    "Order_ID",
    "Transaction_ID",
    "Payment_Method",
    "Payment_Amount",
    "Payment_Date",
    "Payment_Status"
)

# COMMAND ----------

payments_df.count()

# COMMAND ----------

from pyspark.sql.functions import col

payments_df.groupBy("Payment_ID") \
    .count() \
    .filter(col("count") > 1) \
    .count()

# COMMAND ----------

fact_payments_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/facts/fact_payments")

display(fact_payments_df)