import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv(override=True)


TABLES = [
    "FACT_SALES",
    "FACT_PAYMENTS",
    "FACT_RETURNS",
    "FACT_REVIEWS",
    "FACT_SHIPMENTS",
    "DIM_CUSTOMER",
    "DIM_PRODUCT",
    "DIM_SELLER",
    "DIM_WAREHOUSE",
]


def reset_warehouse():
    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database="REATILPULSE_DW",
        schema="REATILPULSE_SCHEMA",
        role=os.getenv("SNOWFLAKE_ROLE")
    )

    cur = conn.cursor()

    try:
        print("\n" + "=" * 70)
        print("RESETTING SNOWFLAKE WAREHOUSE TABLES")
        print("=" * 70)

        for table in TABLES:
            print(f"Clearing: {table}")
            cur.execute(f"TRUNCATE TABLE {table}")

        print("Warehouse tables cleared successfully.")

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    reset_warehouse()
    