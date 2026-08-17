# Databricks notebook source
return_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Returns.parquet"
)

display(return_df)

# COMMAND ----------

return_df.count()

# COMMAND ----------

"Check Duplicates"

dup_df = return_df.count() - return_df.dropDuplicates().count()

display(dup_df)

# COMMAND ----------

"Duplicate Return_id"

from pyspark.sql.functions import col

dup_return_id = return_df.groupBy("Return_ID") \
    .count() \
    .filter(col("count") > 1)

display(dup_return_id)

# COMMAND ----------

"Null Values"

from pyspark.sql.functions import col,sum

null_value = return_df.select(
    [sum(col(c).isNull().cast("int")).alias (c) for c in  return_df.columns]
)

display(null_value)

# COMMAND ----------

"Empty Value"

from pyspark.sql.functions import col,trim
empty_val_df =return_df.filter(
    (trim(col("Return_Reason")) == "")|
    (trim(col("Return_Reason")).rlike("^[0-9]+$"))|
    (trim(col("Return_Status")) == "")
)

display(empty_val_df)

# COMMAND ----------

return_df.printSchema()


# COMMAND ----------

return_df.select("Return_Status").distinct().show(truncate = False)

# COMMAND ----------

from pyspark.sql.functions import regexp_replace, col

returns_df = return_df.withColumn(
    "Return_Status",
    regexp_replace(col("Return_Status"), r"[\r\n\t]", "")
)

# COMMAND ----------

returns_df.select("Return_Status").distinct().display()

# COMMAND ----------

returns_df.selectExpr(
    "Return_Status",
    "length(Return_Status) as Length",
    "hex(Return_Status) as HEX"
).display()

# COMMAND ----------

from pyspark.sql.functions import instr

returns_df.select(
    instr("Return_Status", "\r").alias("contains_cr")
).groupBy("contains_cr").count().show()

# COMMAND ----------

from pyspark.sql.functions import when, col

returns_df = returns_df.withColumn(
    "Return_Status",
    when(col("Return_Status") == "Done", "Completed")
    .when(col("Return_Status") == "Processing", "In Progress")
    .otherwise(col("Return_Status"))
)

display(returns_df)

# COMMAND ----------

returns_df.select("Return_Status").distinct().show(truncate=False)

# COMMAND ----------

from pyspark.sql.functions import hex, col

returns_df.select(
    col("Return_Status"),
    hex(col("Return_Status")).alias("HEX")
).distinct().show(truncate=False)

# COMMAND ----------

returns_df.filter(col("Return_Status").contains("\r")).count()

# COMMAND ----------


from pyspark.sql.functions import col, trim

valid_rs = [
    "Requested",
    "Approved",
    "Rejected",
    "Completed",
    "Cancelled",
    "In Progress"
]

invalid_rs = returns_df.filter(
    ~trim(col("Return_Status")).isin(valid_rs)
)

display(invalid_rs)

# COMMAND ----------

"Invalid Date"
from pyspark.sql.functions import col,current_date

date = return_df.filter(
    (col("Return_Date") > current_date())
)

display(date)

# COMMAND ----------

"Negative Refund_Amount"

negative_rfam = return_df.filter(col("Refund_Amount") < 0)
display(negative_rfam)

# COMMAND ----------

order_df = spark.read.parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/orders.parquet/")

# COMMAND ----------

"Foreign Key Validation (Order_ID → Orders"

check_fk = return_df.join(
    order_df.select("Order_ID"),
    on = "Order_ID",
    how = "left_anti"
)

display(check_fk )

# COMMAND ----------

'''Transformation 
Remove Duplicates'''

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, col

window_spec = Window.partitionBy("Return_ID").orderBy(col("Return_ID"))

return_df = (
    return_df
    .withColumn("rn", row_number().over(window_spec))
    .filter(col("rn") == 1)
    .drop("rn")
)

# COMMAND ----------

print(return_df.count())

# COMMAND ----------

type(return_df)

# COMMAND ----------

"Trim for string Columns"

from pyspark.sql.functions import col,trim

for column_name,datatype in return_df.dtypes:
    if datatype == "string":
        return_df = return_df.withColumn(
            "column_name",
            trim(col(column_name))
        ) 

# COMMAND ----------

from pyspark.sql.functions import col,regexp_replace

for column_name,datatype in return_df.dtypes:
    if datatype == "string":
        return_df = return_df.withColumn(
            "column_name",
            regexp_replace(
                regexp_replace(col(column_name),"\r",""),"\n","")
            )

# COMMAND ----------

"Standardize text columns"

from pyspark.sql.functions import col,initcap,lower

for column_name in ["Return_Reason", "Return_Status"]:
    return_df = return_df.withColumn(
        "column_name",
    initcap(lower(col(column_name))))

# COMMAND ----------

"Replace invalid  return status values with NULL"

from pyspark.sql.functions import col,when

valid_rv = [
    "Approved",
    "Completed",
    "Requested",
    "Rejected",
    "Processing"
]

invalid_rv = return_df.withColumn(
    "Return_Status",
    when(
    col("Return_Status") .isin(valid_rv),
    col("Return_Status")
).otherwise(None)
)

display(invalid_rv)

# COMMAND ----------

from pyspark.sql.functions import col, when

return_df = return_df.withColumn(
    "Return_Status",
    when(col("Return_Status") == "Open", "Pending")
    .when(col("Return_Status") == "Done", "Approved")
    .otherwise(col("Return_Status"))
)

display(return_df )

# COMMAND ----------

return_df.printSchema()

# COMMAND ----------



# COMMAND ----------

returns_df = returns_df.drop("column_name")

# COMMAND ----------

returns_df.columns

# COMMAND ----------

"Validate Order_ID"

valid_oi = return_df.join(
    order_df.select("Order_ID").distinct(),
    on = "Order_ID",
    how = "left_anti"
)
display(valid_oi)

# COMMAND ----------

from pyspark.sql.functions import when, col

returns_df = returns_df.withColumn(
    "Return_Status",
    when(col("Return_Status") == "Done", "Completed")
    .otherwise(col("Return_Status"))
)

# COMMAND ----------

returns_df.select("Return_Status").distinct().show(truncate=False)

# COMMAND ----------

returns_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/returns.parquet")

# COMMAND ----------

returns_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/returns.parquet"
)

returns_df.select("Return_Status").distinct().show(truncate=False)

# COMMAND ----------

returns_check = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/returns.parquet"
)

returns_check.filter(col("Return_Status") == "Done").show()

# COMMAND ----------

saved_returns_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/returns.parquet"
)

display(saved_returns_df)