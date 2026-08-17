import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# Load environment variables
load_dotenv()

# Connect to Snowflake
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

# Read Parquet
path = r"E:\RetailPulse-ETL-Data_Platform\data\warehouse\Facts\fact_returns"

df = pd.read_parquet(path)

print("Rows:", len(df))

# Convert column names to uppercase
df.columns = [col.upper() for col in df.columns]

# Load into Snowflake
success, nchunks, nrows, output = write_pandas(
    conn,
    df,
    "FACT_RETURNS"
)

print("Load Success:", success)
print("Rows Loaded:", nrows)

conn.close()

print("✅ Connection Closed")