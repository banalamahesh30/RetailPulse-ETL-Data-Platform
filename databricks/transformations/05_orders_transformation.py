# Databricks notebook source
order_df = spark.read.parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/Orders.parquet")
display(order_df)

# COMMAND ----------

order_df.count()

# COMMAND ----------

"Duplicate Orders"

duplicate_orders = order_df.count() - order_df.dropDuplicates().count()
display(duplicate_orders)

# COMMAND ----------

from pyspark.sql.functions import *

duplicate_oid = order_df.groupBy("Order_ID") \
                        .count() \
                        .filter(col("count") > 1)

display(duplicate_oid)




# COMMAND ----------

duplicate_oid.count()

# COMMAND ----------

" Empty "
from pyspark.sql.functions import *

empty_order_df = order_df.filter(trim("Shipping_Address") == "")
display(empty_order_df)

# COMMAND ----------

"Null"

from pyspark.sql.functions import *

null_df = order_df.select(
    [sum(col(c).isNull().cast("int")).alias(c) for c in order_df.columns ]
    ).show()

# COMMAND ----------

"Check Empty In Order_Status"

empty_os = order_df.filter(trim("Payment_status") == "Unknown")

display(empty_os)

# COMMAND ----------

order_df.printSchema()

# COMMAND ----------

" Delete Duplicates "


from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, col

window_spec = Window.partitionBy("Order_ID").orderBy(col("Order_ID"))

order_df = (
    order_df
    .withColumn("rn", row_number().over(window_spec))
    .filter(col("rn") == 1)
    .drop("rn")
)

# COMMAND ----------


order_df.count()

# COMMAND ----------

from pyspark.sql.functions import col

order_df.groupBy("Order_ID") \
    .count() \
    .filter(col("count") > 1) \
    .count()

# COMMAND ----------

from pyspark.sql.functions import lower,col
clean_o = order_df.filter(lower(col("Order_Status")) == "delivery")
display(clean_o)

# COMMAND ----------

from pyspark.sql.functions import initcap,trim,col

clean_order_df = order_df.withColumn(
    "Order_Status",
    initcap(lower(col("Order_Status"))) 
)
display(clean_order_df)

# COMMAND ----------

clean_payment = order_df.filter(col("Order_Total") < 0)
display(clean_payment)

# COMMAND ----------

from pyspark.sql.functions import to_date,col

orders_clean_df = order_df.withColumn(
    "Order_Date",
    to_date(col("Order_Date"), "yyyy-MM-dd")
)

display(orders_clean_df)

# COMMAND ----------

order_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/orders.parquet")

# COMMAND ----------

order_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/orders.parquet"
)

# COMMAND ----------

order_df.count()

# COMMAND ----------

drop_dupli_oid = order_df.groupBy("Order_ID") \
                         .count() \
                         .filter(col("count") > 1)
display(drop_dupli_oid)

# COMMAND ----------

saved_orders_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/orders.parquet"
)

print("Saved Orders:", saved_orders_df.count())