import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv(override=True)

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse="RETAILPULSE_WH",
    database="REATILPULSE_DW",
    schema="REATILPULSE_SCHEMA",
    role=os.getenv("SNOWFLAKE_ROLE")
)

print("Connected to Snowflake successfully!")

cur = conn.cursor()

tables = [
    "DIM_CUSTOMER",
    "DIM_DATE",
    "DIM_PRODUCT",
    "DIM_SELLER",
    "DIM_WAREHOUSE",
    "FACT_SALES",
    "FACT_PAYMENTS",
    "FACT_RETURNS",
    "FACT_REVIEWS",
    "FACT_SHIPMENTS"
]

for table in tables:
    print("\n" + "=" * 60)
    print(table)
    print("=" * 60)

    cur.execute(f"DESCRIBE TABLE {table}")

    for row in cur.fetchall():
        print(f"{row[0]:30} | {row[1]:20}")

cur.close()
conn.close()

print("\nConnection closed.")