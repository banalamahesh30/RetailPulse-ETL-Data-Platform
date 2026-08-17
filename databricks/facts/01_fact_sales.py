# Databricks notebook source
orders_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/orders.parquet"
)

order_items_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/order_items.parquet"
)

# COMMAND ----------

fact_sales_df = orders_df.join(
    order_items_df,
    on="Order_ID",
    how="inner"
)

# COMMAND ----------

fact_sales_df = fact_sales_df.select(
    "Order_Item_ID",
    "Order_ID",
    "Customer_ID",
    "Product_ID",
    "Order_Date",
    "Quantity",
    "Unit_Price",
    "Discount",
    "Tax",
    "Total_Amount",
    "Order_Total",
    "Order_Status",
    "Payment_Status"
)

# COMMAND ----------

fact_sales_df.count()

# COMMAND ----------

from pyspark.sql.functions import col

fact_sales_df.groupBy("Order_Item_ID") \
    .count() \
    .filter(col("count") > 1) \
    .count()

# COMMAND ----------

fact_sales_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/facts/fact_sales")