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


# DIM_CUSTOMER parquet folder path
file_path = r"E:\RetailPulse-ETL-Data_Platform\data\warehouse\Dimension\dim_customer\dim_customer"


# Read Spark parquet folder
df = pd.read_parquet(file_path)

print("Rows before transformation:", len(df))


# Create CUSTOMER_NAME column
df["CUSTOMER_NAME"] = (
    df["First_Name"] + " " + df["Last_Name"]
)


# Select columns matching Snowflake table
df = df[
    [
        "Customer_ID",
        "CUSTOMER_NAME",
        "Email",
        "Phone",
        "Gender",
        "Date_of_Birth",
        "City",
        "State",
        "Country",
        "Postal_Code",
        "Registration_Date",
        "Customer_Status"
    ]
]


# Convert column names to uppercase for Snowflake
df.columns = [col.upper() for col in df.columns]


print("Final columns:")
print(df.columns)

print("Rows to load:", len(df))


# Load data into Snowflake
success, nchunks, nrows, output = write_pandas(
    conn,
    df,
    "DIM_CUSTOMER"
)


print("Load Success:", success)
print("Rows Loaded:", nrows)


# Close connection
conn.close()

print("✅ Connection closed")