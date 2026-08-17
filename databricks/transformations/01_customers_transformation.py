# Databricks notebook source
display(dbutils.fs.ls("/Volumes/workspace/retailpulse_data/retailpulse_volume"))

# COMMAND ----------

customers_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/customers.parquet"
)

display(customers_df)

# COMMAND ----------

customers_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/customers.parquet"
)

# COMMAND ----------

products_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Products.parquet"
)

payments_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Payments.parquet"
)

shipments_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Shipments.parquet"
)

returns_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Returns.parquet"
)

reviews_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Reviews.parquet"
)

sellers_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Sellers.parquet"
)

warehouse_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Warehouse.parquet"
)

# COMMAND ----------

customers_df.count()


# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
customers_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/customers.parquet"
)

# COMMAND ----------

display(customers_df.limit (10))

# COMMAND ----------

'''Check a Duplicate Rows'''

duplicate_count = customers_df.count() - customers_df.dropDuplicates().count()
print (f"Duplicate Records : {duplicate_count}")

# COMMAND ----------

'''Check Null Values'''
from pyspark.sql.functions import col,sum
customers_df.select(
    [sum(col(c).isNull().cast("int")).alias(c) for c in customers_df.columns]
).show()

# COMMAND ----------

'''Check a Null Emails'''
from pyspark.sql.functions import * 

customers_df.filter(trim("email")=="").count()

# COMMAND ----------

'''Check a Duplicates Customer_id '''

from pyspark.sql.functions import col

duplicate_df= customers_df.groupBy("Customer_ID")\
                          .count()\
                          .filter(col("count") > 1)

display(duplicate_df)

# COMMAND ----------

'''Data Types'''

customers_df.printSchema()

# COMMAND ----------

'''Invalid Data'''

from pyspark.sql.functions import trim

empty_cname_df = customers_df.filter(trim(col("First_Name")) =="")

display(empty_cname_df)



                           

# COMMAND ----------

"Empty Email"

empty_email_df = customers_df.filter(trim(col("Email"))== "")


display(empty_email_df)


# COMMAND ----------

"Invalid Email"

invalid_email_df =customers_df.filter(~col("Email").rlike(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"))

display(invalid_email_df)

# COMMAND ----------

invalid_email_df.show(1000, truncate = False)

# COMMAND ----------

"Apply Transformations"

from pyspark.sql.functions import trim, lower,col

customers_clean_df = customers_df.dropDuplicates()

for column_name,data_type in customers_clean_df.dtypes:
    if data_type == "string":
        customers_clean_df = customers_clean_df.withColumn(
            column_name,
                trim(col(column_name))
        )

customers_clean_df = customers_clean_df.withColumn(
    "Email",
    lower(col("Email"))
)


# COMMAND ----------

display(customers_clean_df)

# COMMAND ----------

customers_clean_df.count()

# COMMAND ----------

customers_clean_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/customers.parquet")

# COMMAND ----------

customers_verify_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/customers.parquet"
)

# COMMAND ----------

display(dbutils.fs.ls("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed"))

# COMMAND ----------

customers_verify_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/customers.parquet"
).count()

display(customers_verify_df)

# COMMAND ----------

from pyspark.sql.functions import col, trim

customers_clean_df.filter(trim(col("Email")) == "").count()
