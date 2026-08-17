# Databricks notebook source
order_items_df = spark.read.parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/Orders_items.parquet")
display(order_items_df)

# COMMAND ----------

order_items_df.count()

# COMMAND ----------

dup_oi = order_items_df.count() - order_items_df.dropDuplicates().count()
display(dup_oi)

# COMMAND ----------

" Duplicate Order Id" 
from pyspark.sql.functions import col

dup_oi_df = order_items_df.groupBy("Order_Item_ID") \
                        .count() \
                        .filter(col("count") > 1)
display(dup_oi_df)

# COMMAND ----------

"Duplicate Product Id"
dup_pi_df = order_items_df.groupBy("Product_ID") \
                          .count() \
                          .filter(col("count") > 1)

display(dup_pi_df)

# COMMAND ----------

from pyspark.sql.functions import col

order_items_df.groupBy("Order_Item_ID") \
    .count() \
    .filter(col("count") > 1) \
    .count()

# COMMAND ----------

order_items_df.printSchema()

# COMMAND ----------

"Null Values"
from pyspark.sql.functions import col,sum

empty_oi_df = order_items_df.select(
    [sum(col(c).isNull().cast("int")).alias(c) for c in  order_items_df.columns ]
).show()

# COMMAND ----------

"Invalid Quantity"

from pyspark.sql.functions import col

invalid_quntity = order_items_df.filter(
    col("Quantity") < 0
)

display(invalid_quntity)

# COMMAND ----------

"Invalid Unit Price"

invalid_unit_price = order_items_df.filter(col("Unit_Price") < 0)
display(invalid_unit_price)

# COMMAND ----------

"Invalid Total "

from pyspark.sql.functions import round,col
invalid_total_cal_df = (
    order_items_df.withColumn("Current_total",
        round(
            (
                col("Quantity") * col("Unit_Price") 
            - col("Discount")
            + col("Tax")
            ),
            2
        )
    )
    .filter(
        col("current_total")!= round(col("Total_Amount"), 2)
        )
        .orderBy("Order_Item_ID")
)

    

display(invalid_total_cal_df)

# COMMAND ----------

invalid_total_cal_df.count()

# COMMAND ----------

from pyspark.sql.functions import col, round

invalid_total_cal_df = (
    order_items_df
    .withColumn(
        "Calculated_Total",
        round(
            (
                col("Quantity") * col("Unit_Price")
                - col("Discount")
                + col("Tax")
            ),
            2
        )
    )
    .filter(
        col("Calculated_Total") != round(col("Total_Amount"), 2)
    )
    .orderBy("Order_Item_ID")
)

display(invalid_total_cal_df)

# COMMAND ----------

orders_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/orders.parquet"
)

products_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/products.parquet"
)

# COMMAND ----------

" Foreign Key Validation Order_ID "

invalid_order_fk_df = order_items_df.join(
   orders_df.select("Order_ID"),
   on = "Order_ID",
   how = "left_anti"

)
display(invalid_product_fk_df)

# COMMAND ----------


invalid_product_fk_df.count()

# COMMAND ----------

" Foreign Key Validation Product_ID "

invalid_product_fk_df = order_items_df.join(
    products_df.select("Product_ID"),
    on = "Product_ID",
    how = "left_anti"
)

display(invalid_product_fk_df)

# COMMAND ----------

invalid_product_fk_df.count()

# COMMAND ----------

"Remove exact duplicate rows"

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, col

window_spec = Window.partitionBy("Order_Item_ID").orderBy(col("Order_Item_ID"))

order_items_df = (
    order_items_df
    .withColumn("rn", row_number().over(window_spec))
    .filter(col("rn") == 1)
    .drop("rn")
)

# COMMAND ----------

order_items_df.groupBy("Order_Item_ID") \
    .count() \
    .filter(col("count") > 1) \
    .count()

# COMMAND ----------

"Validate/Fix numeric fields"

from pyspark.sql.functions import col

valid_df = order_items_df.filter(
    (col("Quantity") > 0)&
    (col("Unit_Price") > 0)&
    (col("Discount") > 0)&
    (col("Tax") > 0)&
    (col("Total_Amount") > 0)
)

display(valid_df)

# COMMAND ----------

"Validate relationships with Orders "

order_items_clean_df = order_items_df.join(
    orders_df.select("Order_ID"),
    on = "Order_ID",
    how = "Inner"
)
order_items_clean_df = order_items_df.join(
    products_df.select("Product_ID"),
    on = "Product_ID",
    how = "Inner"
)

display(order_items_clean_df)
display(order_items_clean_df)


# COMMAND ----------


order_items_clean_df.count()


# COMMAND ----------

order_items_df.write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/order_items.parquet")



# COMMAND ----------

order_items_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/order_items.parquet"
)

# COMMAND ----------

order_items_df.count()