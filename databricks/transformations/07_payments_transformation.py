# Databricks notebook source
payments_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Payments.parquet"
)

display(payments_df)

# COMMAND ----------

payments_df.count()

# COMMAND ----------

"Duplicate Payments"

dup_payments_df = payments_df.count() - payments_df.dropDuplicates().count()
display(dup_payments_df )

# COMMAND ----------

"empty and transaction_id and payment_method"
from pyspark.sql.functions import col,trim

empty_ti_pm_df = payments_df.filter( 
    (
        col("Transaction_ID").isNull() |
        (trim("Transaction_ID")=="")
    )&
    (
        col("Payment_Method").isNull() |
        (trim("Payment_Method")== "")
    )&
    (
        col("Payment_Status").isNull() |
        (trim("Payment_Status") == "")
    )
) 

display(empty_ti_pm_df)

# COMMAND ----------

"empty and transaction_id and payment_method"

empty_pm_ti_df = payments_df.filter(
    (trim("Transaction_ID") == "") |
    (trim("Payment_Method") == "") |
    (trim("Payment_Status") == "")
)

display(empty_pm_ti_df)

# COMMAND ----------

from pyspark.sql.functions import col, trim

empty_df = payments_df.filter(
    (
        col("Transaction_ID").isNull() |
        (trim(col("Transaction_ID")) == "")
    ) &
    (
        col("Payment_Method").isNull() |
        (trim(col("Payment_Method")) == "")
    )
)

display(empty_df)

# COMMAND ----------

"Data trype"

payments_df.printSchema()

# COMMAND ----------

'''Invalid Data
Negative payment amount
'''

invalid_data = payments_df.filter(
    (col("Payment_Amount") < 0) 
)
display(invalid_data)

# COMMAND ----------

order_df = spark.read.parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/orders.parquet/")

# COMMAND ----------

"Invalid Order_id"

invalid_order_id = payments_df.join(
    order_df.select("Order_ID"),
    on = "Order_ID",
    how = "leftanti"
)
display(invalid_order_id)


# COMMAND ----------


invalid_order_id.count()

# COMMAND ----------

payments_clean_df = payments_df.join(
    order_df.select("Order_ID"),
    on="Order_ID",
    how="inner"
)
display(payments_clean_df)

# COMMAND ----------

payments_clean_df.count()

# COMMAND ----------

from pyspark.sql.functions import trim,col
for column_name, data_type in payments_clean_df.dtypes:
    if data_type == "string":
        payments_clean_df = payments_clean_df.withColumn(
            column_name,
            trim(col(column_name))
        )


# COMMAND ----------

payments_df.coalesce(1).write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/payments.parquet")