# Databricks notebook source
shipments_df = spark.read.parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/Shipments.parquet")
display(shipments_df)

# COMMAND ----------

shipments_df.count()

# COMMAND ----------

dup_df = shipments_df.count() - shipments_df.dropDuplicates().count()

display(dup_df)

# COMMAND ----------

"Empty Tracking Number"

from pyspark.sql.functions import trim,col
empty_tn_df = shipments_df.filter(
    (trim(col("Tracking_Number")) == "") |
    (trim(col("Shipment_Status")) == "") 
)
display(empty_tn_df)

# COMMAND ----------

shipments_df.printSchema()

# COMMAND ----------

shipments_df.select("Shipment_Status").distinct().show(truncate = False)

# COMMAND ----------

"Invalid Shipment"

from pyspark.sql.functions import col

valid_ship_df = [
    "Shipped",
    "In Transit",
    "Delivered",
    "Cancelled",
    "Returned"
]

invalid_ship_df = shipments_df.filter(
        ~col("Shipment_Status").isin(valid_ship_df)
)

display(invalid_ship_df)

# COMMAND ----------

order_df = spark.read.parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/orders.parquet/")

# COMMAND ----------

"Check Relation"
relation = shipments_df.join(
    order_df.select("Order_ID").distinct(),
    on = "Order_ID",
    how = "left_anti"
)

display(relation)

# COMMAND ----------

"trim all string columns"

from pyspark.sql.functions import trim, col


shipment_clean_df = shipments_df.dropDuplicates()
for column_name,datatype in shipment_clean_df.dtypes:
    if datatype == "String":
        shipment_clean_df = shipment_clean_df.withColumn(
            column_name,
            trim(col("column_name"))

        )
        


# COMMAND ----------

"Remove hidden characters"

from pyspark.sql.functions import  col,regexp_replace
for column_name,datatype in shipment_clean_df.dtypes:
    if datatype == "String":
        shipment_clean_df = shipment_clean_df.withColumn(
            column_name,
            regexp_replace(col(column_name), "\r", "")
        )

# COMMAND ----------

"Valid Order_id"

valid_oi = shipments_df.join(
    order_df.select("Order_ID"),
    on = 'Order_ID',
    how = "inner"

)

# COMMAND ----------

from pyspark.sql.functions import col, regexp_replace, trim

shipments_df = shipments_df.withColumn(
    "Shipment_Status",
    trim(regexp_replace(col("Shipment_Status"), "\r", ""))
)

# COMMAND ----------

"clean shipment status"
from pyspark.sql.functions import col,when

clean_ship_status_df = shipments_df.withColumn(
    "Shipment_Status",
    when(col("Shipment_Status") == "Deliveredd", "Delivered")
    .when(col("Shipment_Status") == "Moving", "In Transit")
    .when(col("Shipment_Status") == "On Way", "In Transit")
    .otherwise(col("Shipment_Status"))
)
display(
clean_ship_status_df)

# COMMAND ----------

clean_ship_status_df.select("Shipment_Status").distinct().show(truncate=False)

# COMMAND ----------

shipments_df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import col


check = [
    "Shipped",
    "In Transit",
    "Delivered",
    "Cancelled",
    "Returned"
]

checking = clean_ship_status_df.filter(
    ~col("Shipment_Status").isin(check)
)
display(checking)

# COMMAND ----------

shipments_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/shipments.parquet")

# COMMAND ----------

saved_shipments_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/shipments.parquet"
)

display(saved_shipments_df)