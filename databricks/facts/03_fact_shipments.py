# Databricks notebook source
shipments_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/shipments.parquet"
)

# COMMAND ----------

shipments_df.printSchema()

# COMMAND ----------

fact_shipments_df = shipments_df.select(
    "Shipment_ID",
    "Order_ID",
    "Warehouse_ID",
    "Tracking_Number",
    "Courier",
    "Shipment_Date",
    "Delivery_Date",
    "Shipment_Status"
)

# COMMAND ----------

fact_shipments_df.count()

# COMMAND ----------

from pyspark.sql.functions import col

fact_shipments_df.groupBy("Shipment_ID") \
    .count() \
    .filter(col("count") > 1) \
    .count()

# COMMAND ----------

fact_shipments_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/facts/fact_shipments")

# COMMAND ----------

fact_shipments_check = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/facts/fact_shipments"
)

display(fact_shipments_check)