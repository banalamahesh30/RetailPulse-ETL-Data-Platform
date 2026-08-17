# Databricks notebook source
sellers_df = spark.read.parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/Sellers.parquet")
display(sellers_df)

# COMMAND ----------

"Duplicate Records"

duplicates_df = sellers_df.count() - sellers_df.dropDuplicates().count()
print(f"Duplicate Seller Records : {duplicates_df}")


# COMMAND ----------

from pyspark.sql.functions import *

duplicate_sid = sellers_df.groupBy("Seller_ID") \
          .count() \
          .filter(col("count")> 1)

display(duplicate_sid)

# COMMAND ----------

"Null Or Empty Email"

from pyspark.sql.functions import *
empty_email_df = sellers_df.filter(trim("Email") == "")

display(empty_email_df)


# COMMAND ----------

"Null Or Empty Contact Name"

empty_contact_name_df = sellers_df.filter(trim("Contact_Name") == "")

display(empty_contact_name_df)

# COMMAND ----------

"Invalid Emails "

invalid_email_df = sellers_df.filter(~col("Email").rlike(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"))

display(invalid_email_df)

# COMMAND ----------

sellers_df.printSchema()

# COMMAND ----------

"Invalid Mobile Number"

invalid_num_df = sellers_df.filter(~col("Phone").rlike (r"^[0-9]{10}$"))

display(invalid_num_df)

# COMMAND ----------

"Apply Transformation "

clean_seller_df = sellers_df.dropDuplicates()

for column_name,datatype in clean_seller_df.dtypes:
    if datatype == "string":
        clean_seller_df = clean_seller_df.withColumn(
            column_name,
            trim(col(column_name))
        )

clean_seller_df = clean_seller_df.withColumn(
    "Email",
    lower(col("Email"))
)

display(clean_seller_df)

# COMMAND ----------

clean_seller_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/sellers.parquet")

# COMMAND ----------

