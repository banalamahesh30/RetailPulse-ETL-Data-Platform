import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


load_dotenv()


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


file_path = r"E:\RetailPulse-ETL-Data_Platform\data\warehouse\Dimension\dim_warehouse\dim_warehouse"


df = pd.read_parquet(file_path)

print("Rows before transformation:", len(df))

print(df.columns)


# Convert columns to uppercase
df.columns = [col.upper() for col in df.columns]


df = df[
    [
        "WAREHOUSE_ID",
        "WAREHOUSE_NAME",
        "ADDRESS",
        "CITY",
        "STATE",
        "COUNTRY",
        "POSTAL_CODE",
        "CAPACITY",
        "MANAGER_NAME",
        "CONTACT_NUMBER",
        "WAREHOUSE_STATUS"
    ]
]


print("Rows to load:", len(df))


success, nchunks, nrows, output = write_pandas(
    conn,
    df,
    "DIM_WAREHOUSE"
)


print("Load Success:", success)
print("Rows Loaded:", nrows)


conn.close()

print("✅ Connection closed")