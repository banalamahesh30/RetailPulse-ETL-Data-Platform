# Databricks notebook source
warehouse_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Warehouse.parquet"
)
display(warehouse_df)

# COMMAND ----------

warehouse_df.count()

# COMMAND ----------

"Checking Duplicates"
dup = warehouse_df.count() - warehouse_df.dropDuplicates().count()
display(dup)

# COMMAND ----------

"Null Values"
from pyspark.sql.functions import sum,col

null = warehouse_df.select(
    [sum(col(c).isNull().cast("int")).alias (c) for c in warehouse_df.columns]
)
display(null)

# COMMAND ----------

"Empty"

from pyspark.sql.functions import trim,col,when

empty = warehouse_df.select(
    [sum(when(trim(col(c)) == "",1).otherwise(0)).alias(c)
     for c in warehouse_df.columns ]).show(truncate = False)
     

# COMMAND ----------

"Invalid Capacity"

from pyspark.sql.functions import col

invalid_capacity = warehouse_df.filter(col("Capacity") < 0)

display(invalid_capacity )


# COMMAND ----------

"trim string columns"

from pyspark.sql.functions import trim,col

for column_name,datatype in warehouse_df.dtypes:
    if datatype == "string":
        warehouse_df = warehouse_df.withColumn(
            "column_name",
            trim(col(column_name))
        )

# COMMAND ----------

"Remove hidden characters (\r, \n, \t)"

from pyspark.sql.functions import regexp_replace,col

for column_name,datatype in warehouse_df.dtypes:
    if datatype == "string":
        warehouse_df = warehouse_df.withColumn(
            column_name,
                regexp_replace(col(column_name),r"[\r\n\t]", "")
        )



# COMMAND ----------

from pyspark.sql.functions import col, trim

invalid_location_df = warehouse_df.filter(
    col("City").isNull() |
    (trim(col("City")) == "") |
    col("State").isNull() |
    (trim(col("State")) == "")
)

display(invalid_location_df)

# COMMAND ----------

"Delete negative capacity"
from pyspark.sql.functions import col

warehouse_df = warehouse_df.filter(
    col("Capacity") >= 0
)

# COMMAND ----------

warehouse_clean_df = warehouse_df

warehouse_clean_df.coalesce(1).write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/warehouses.parquet")

# COMMAND ----------

warehouse_clean_df.count()