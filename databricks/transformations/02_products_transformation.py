# Databricks notebook source
Product_df = spark.read.parquet(
     "/Volumes/workspace/retailpulse_data/retailpulse_volume/Products.parquet"

)

display(Product_df)

# COMMAND ----------

Product_df.count()

# COMMAND ----------

"Check How Many Duplicate Products"

Duplicate_Product_df = Product_df.count() - Product_df.dropDuplicates().count()

print (f"Duplicate Products : {Duplicate_Product_df}")

# COMMAND ----------

"Check Duplicate Product"

from pyspark.sql.functions import *

Duplicate_ids = Product_df.groupBy("Product_ID") \
                              .count() \
                              .filter(col("count") >1 )\
                              .select("Product_ID")

Duplicate_Products = Product_df.join(
    Duplicate_ids,
    on = "Product_ID",
    how = "Inner"
)

display(Duplicate_Products)

# COMMAND ----------

Duplicate_id = Product_df.groupBy("Product_ID") \
                .count() \
                .filter(col("count") > 1)
                
display(Duplicate_id)

# COMMAND ----------

"Check Null Products"



null_products_df = Product_df.select(
    [sum(col(c).isNull().cast("int")).alias(c) for c in Product_df.columns]
)

display(null_products_df)

# COMMAND ----------

"Check Empty Values"

empty_df = Product_df.filter(trim(col("Brand")) == "")

empty_df.count()
display(empty_df)

# COMMAND ----------

"Data Type"

Product_df.printSchema()

# COMMAND ----------

Product_df = Product_df.dropDuplicates()

# COMMAND ----------

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, col

window_spec = Window.partitionBy("Product_ID").orderBy(col("Seller_ID"))

Product_df = (
    Product_df
    .withColumn("rn", row_number().over(window_spec))
    .filter(col("rn") == 1)
    .drop("rn")
)

# COMMAND ----------

Product_df.count()

# COMMAND ----------

"Remove /r /n"

from pyspark.sql.functions import regexp_replace,col

for column_name,datatype in Product_df.dtypes:
    if datatype == "string":
        Product_df = Product_df.withColumn(
            column_name,
            regexp_replace(col(column_name),r"[\r\n\t]", "")
        )

# COMMAND ----------

Product_df.select("Product_Status").distinct().show(truncate=False)

# COMMAND ----------

"Invalid Data"

from pyspark.sql.functions import *

Product_df = Product_df.dropDuplicates()

for column_name,data_type in Product_df.dtypes:
        if data_type == "string":
            product_clean_df = Product_df.withColumn(
                column_name,
                trim(col(column_name))
            )

display(Product_df)

# COMMAND ----------

"Standardize text"
from pyspark.sql.functions import col,trim,initcap,lower

Product_df = Product_df.withColumn(
    "Category",
    initcap(lower(col("Category")))
)

display(Product_df)

# COMMAND ----------

from pyspark.sql.functions import col

Product_df = Product_df.filter(
    (col("Price") >= 0) &
    (col("Cost_Price") >= 0) &
    (col("Stock") >= 0) &
    (col("Weight") >= 0)
)

display(Product_df )

# COMMAND ----------

sellers_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Sellers.parquet"
)

# COMMAND ----------

"Validate Seller_ID"

Product_df = Product_df.join(
    sellers_df.select("Seller_ID"),
    on = "Seller_ID",
    how = "left_anti"

)

display(Product_df)

# COMMAND ----------

Product_df.count()

# COMMAND ----------

Product_df. coalesce(1).write \
    .mode("overwrite") \
    .parquet("/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/products.parquet")

    

# COMMAND ----------

Product_df.count()