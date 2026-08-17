from config.snowflake_config import get_connection

tables = [
    "DIM_CUSTOMER",
    "DIM_PRODUCT",
    "DIM_SELLER",
    "DIM_WAREHOUSE",
    "DIM_DATE",
    "FACT_SALES",
    "FACT_PAYMENTS",
    "FACT_SHIPMENTS",
    "FACT_RETURNS",
    "FACT_REVIEWS"
]

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("USE DATABASE REATILPULSE_DW")
    cursor.execute("USE SCHEMA REATILPULSE_SCHEMA")

    for table in tables:
        print(f"\n{'=' * 50}")
        print(f"TABLE: {table}")
        print("=" * 50)

        cursor.execute(f"DESCRIBE TABLE {table}")

        for row in cursor.fetchall():
            print(f"{row[0]:30} {row[1]}")

finally:
    cursor.close()
    conn.close()