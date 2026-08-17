# Databricks notebook source
reviews_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Reviews.parquet"
)

# COMMAND ----------

reviews_df.show(10, truncate=False)

# COMMAND ----------

reviews_df.printSchema()

# COMMAND ----------

reviews_df.select("Review_Date").show(10, truncate=False)

# COMMAND ----------

from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType

reviews_df = reviews_df.withColumn(
    "Rating",
    col("Rating").cast(IntegerType())
)

display(reviews_df)

# COMMAND ----------

reviews_df.select("Review_Date").show(10, truncate=False)

# COMMAND ----------

from pyspark.sql.functions import col

reviews_df.filter(col("Review_Date").isNull()).count()

# COMMAND ----------

type(reviews_df)

# COMMAND ----------

reviews_df.count()

# COMMAND ----------

"Check Duplicates"

reviews_clean_df = reviews_df.dropDuplicates(["Review_ID"])
reviews_clean_df.count()

# COMMAND ----------

reviews_clean_df = reviews_df.dropDuplicates(["Review_ID"])

print("Before:", reviews_df.count())
print("After:", reviews_clean_df.count())

# COMMAND ----------

reviews_df = reviews_df.toDF(
    "Review_ID",
    "Customer_ID",
    "Product_ID",
    "Rating",
    "Review_Date",
    "Review_Text"
)

# COMMAND ----------

"Null Values"

from pyspark.sql.functions import trim,col,sum

null = reviews_df.select(
    [sum(col(c).isNull().cast("int")).alias(c)for c in reviews_df.columns]
)
display(null)

# COMMAND ----------

reviews_df.printSchema()

# COMMAND ----------

display(reviews_df)

# COMMAND ----------

"Change Rating"


from pyspark.sql.functions import when,col

reviews_df = reviews_df.withColumn(
    "Rating",
    when(col("Rating") == 2021,1)
    .when(col("Rating") == 2022,2)
    .when(col("Rating") == 2023,3)
    .when(col("Rating") == 2024,4)
    .when(col("Rating") == 2025,5)
    .when(col("Rating") == 2026,5)
    .otherwise(col("Rating")))

display(reviews_df)

# COMMAND ----------

from pyspark.sql.functions import col, when, rand, lit

reviews_df = reviews_df.withColumn(
    "Review_Text",
    when(rand() < 0.10, lit(None))
    .when(col("Rating") == 5, "Excellent quality and fast delivery.")
    .when(col("Rating") == 4, "Good product. Value for money.")
    .when(col("Rating") == 3, "Product is okay but delivery was delayed.")
    .when(col("Rating") == 2, "Quality is below expectations.")
    .when(col("Rating") == 1, "Received a damaged product. Very disappointed.")
)

display(reviews_df)

# COMMAND ----------

products_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/Products.parquet"
)

# COMMAND ----------

"Validate Order_ID"

invalid_order_id = reviews_df.join(
    products_df.select("Product_ID"),
    on = "Product_ID",
    how = "left_anti"
)

display(invalid_order_id)

# COMMAND ----------

reviews_clean_df = reviews_df.join(
    products_df.select("Product_ID").distinct(),
    on="Product_ID",
    how="inner"
)

display(reviews_clean_df)

# COMMAND ----------

"Transformation"

"Remove Duplicates"

reviews_df = reviews_df.dropDuplicates()
reviews_df.count()

# COMMAND ----------

print(type(reviews_df))

# COMMAND ----------

"Trim All string columns"

from pyspark.sql.functions import col,trim

for column_name,datatype in reviews_df.dtypes:
    if datatype == "string":
        reviews_df = reviews_df.withColumn(
            column_name,
            trim(col(column_name) == "")
        )

# COMMAND ----------

from pyspark.sql.functions import regexp_replace, col

reviews_clean_df = reviews_df

for c in reviews_clean_df.columns:
    reviews_clean_df = reviews_clean_df.withColumn(
        c,
        regexp_replace(col(c), r"[\r\n\t]", " ")
    )
display(reviews_clean_df)

# COMMAND ----------

reviews_df.filter(
    (col("Rating") < 1) | (col("Rating") > 5)
).show()

# COMMAND ----------

reviews_df = reviews_clean_df.filter(
    (col("Rating") >= 1) &
    (col("Rating") <= 5)
).show()

# COMMAND ----------

print(type(reviews_df))

# COMMAND ----------

print(type(reviews_clean_df))

# COMMAND ----------

reviews_clean_df.coalesce(1).write \
    .mode("overwrite") \
    .parquet(
        "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/reviews.parquet"
    )

# COMMAND ----------

reviews_parquet_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/reviews.parquet"
)

# COMMAND ----------

saved_df = spark.read.parquet(
    "/Volumes/workspace/retailpulse_data/retailpulse_volume/transformed/reviews.parquet"
)

saved_df.count()

# COMMAND ----------

display(dbutils.fs.ls("/Volumes/workspace/retailpulse_data/retailpulse_volume"))

# COMMAND ----------

from pyspark.sql.functions import col

reviews_df.select([
    col(c).isNull().alias(c)
    for c in reviews_df.columns
]).show()