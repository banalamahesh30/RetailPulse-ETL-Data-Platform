# Databricks notebook source
customers_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/customers.parquet"
)
display(customers_df)

# COMMAND ----------

customers_df.printSchema()

# COMMAND ----------

dim_customer_df = customers_df.select(
    "Customer_ID",
    "First_Name",
    "Last_Name",
    "Gender",
    "Date_of_Birth",
    "Email",
    "Phone",
    "Address",
    "City",
    "State",
    "Country",
    "Postal_Code",
    "Registration_Date",
    "Customer_Status"
)

# COMMAND ----------

display(dim_customer_df)

print(dim_customer_df.count())

# COMMAND ----------

from pyspark.sql.functions import col

dim_customer_df.groupBy("Customer_ID") \
    .count() \
    .filter(col("count") > 1) \
    .show()

# COMMAND ----------

dim_customer_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/warehouse/dimensions/dim_customer")