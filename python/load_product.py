import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


# Load .env file
load_dotenv()


# Snowflake connection
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE")
)

print("✅ Connected to Snowflake")


# DIM_PRODUCT parquet folder path
file_path = r"E:\RetailPulse-ETL-Data_Platform\data\warehouse\Dimension\dim_product\dim_product"


# Read parquet folder
df = pd.read_parquet(file_path)

print("Rows before transformation:", len(df))

print("Original columns:")
print(df.columns)


# Convert column names to uppercase
df.columns = [col.upper() for col in df.columns]


# Remove columns that are not required in Snowflake
# (Keep only table columns)
df = df[
    [
        "PRODUCT_ID",
        "PRODUCT_NAME",
        "BRAND",
        "CATEGORY",
        "PRICE",
        "COST_PRICE",
        "STOCK",
        "WEIGHT",
        "LAUNCH_DATE",
        "SELLER_ID",
        "PRODUCT_STATUS"
    ]
]


print("Final columns:")
print(df.columns)

print("Rows to load:", len(df))


# Load data into Snowflake
success, nchunks, nrows, output = write_pandas(
    conn,
    df,
    "DIM_PRODUCT"
)


print("Load Success:", success)
print("Rows Loaded:", nrows)


# Close connection
conn.close()

print("✅ Connection closed")