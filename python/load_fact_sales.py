import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# Load environment variables
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

# Fact Sales parquet folder
path = r"E:\RetailPulse-ETL-Data_Platform\data\warehouse\Facts\fact_sales"

# Read parquet
df = pd.read_parquet(path)

print("Rows before transformation:", len(df))

# Convert column names to uppercase
df.columns = [col.upper() for col in df.columns]

print("Columns:")
print(df.columns)

# Load into Snowflake
success, nchunks, nrows, output = write_pandas(
    conn,
    df,
    "FACT_SALES"
)

print("Load Success:", success)
print("Rows Loaded:", nrows)

conn.close()

print("✅ Connection closed")
