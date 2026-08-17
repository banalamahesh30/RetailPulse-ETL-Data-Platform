# Databricks notebook source
warehouse_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/warehouses.parquet"
)

# COMMAND ----------

warehouse_df.printSchema()

# COMMAND ----------

dim_warehouse_df = warehouse_df.select(
    "Warehouse_ID",
    "Warehouse_Name",
    "Address",
    "City",
    "State",
    "Country",
    "Postal_Code",
    "Capacity",
    "Manager_Name",
    "Contact_Number",
    "Warehouse_Status"
)

# COMMAND ----------

dim_warehouse_df.count()

# COMMAND ----------

from pyspark.sql.functions import col

dim_warehouse_df.groupBy("Warehouse_ID") \
    .count() \
    .filter(col("count") > 1) \
    .show()

# COMMAND ----------

dim_warehouse_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/dimensions/dim_warehouse")