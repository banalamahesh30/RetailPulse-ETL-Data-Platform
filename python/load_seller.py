import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


# Load .env
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


# DIM_SELLER parquet path
file_path = r"E:\RetailPulse-ETL-Data_Platform\data\warehouse\Dimension\dim_seller\dim_seller"


# Read parquet
df = pd.read_parquet(file_path)

print("Rows before transformation:", len(df))

print("Original columns:")
print(df.columns)


# Convert columns to uppercase
df.columns = [col.upper() for col in df.columns]


# Select columns matching Snowflake table
df = df[
    [
        "SELLER_ID",
        "SELLER_NAME",
        "CONTACT_NAME",
        "EMAIL",
        "PHONE",
        "GST_NUMBER",
        "CITY",
        "STATE",
        "POSTAL_CODE",
        "RATING",
        "REGISTRATION_DATE",
        "SELLER_STATUS"
    ]
]


print("Final columns:")
print(df.columns)

print("Rows to load:", len(df))


# Load into Snowflake
success, nchunks, nrows, output = write_pandas(
    conn,
    df,
    "DIM_SELLER"
)


print("Load Success:", success)
print("Rows Loaded:", nrows)


conn.close()

print("✅ Connection closed")