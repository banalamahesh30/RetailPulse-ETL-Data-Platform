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


# ---------------------------------------------------------
# 1. ROW COUNTS
# ---------------------------------------------------------

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

print("\n" + "=" * 60)
print("ROW COUNTS")
print("=" * 60)

for table in tables:

    cur.execute(f"SELECT COUNT(*) FROM {table}")

    count = cur.fetchone()[0]

    print(f"{table:20} : {count:,}")


# ---------------------------------------------------------
# 2. DUPLICATE CHECKS
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("DUPLICATE CHECKS")
print("=" * 60)


duplicate_queries = {

    "DIM_CUSTOMER": """
        SELECT COUNT(*) - COUNT(DISTINCT CUSTOMER_ID)
        FROM DIM_CUSTOMER
    """,

    "DIM_PRODUCT": """
        SELECT COUNT(*) - COUNT(DISTINCT PRODUCT_ID)
        FROM DIM_PRODUCT
    """,

    "DIM_SELLER": """
        SELECT COUNT(*) - COUNT(DISTINCT SELLER_ID)
        FROM DIM_SELLER
    """,

    "DIM_WAREHOUSE": """
        SELECT COUNT(*) - COUNT(DISTINCT WAREHOUSE_ID)
        FROM DIM_WAREHOUSE
    """,

    "FACT_SALES": """
        SELECT COUNT(*) - COUNT(DISTINCT ORDER_ITEM_ID)
        FROM FACT_SALES
    """,

    "FACT_PAYMENTS": """
        SELECT COUNT(*) - COUNT(DISTINCT PAYMENT_ID)
        FROM FACT_PAYMENTS
    """,

    "FACT_RETURNS": """
        SELECT COUNT(*) - COUNT(DISTINCT RETURN_ID)
        FROM FACT_RETURNS
    """,

    "FACT_REVIEWS": """
        SELECT COUNT(*) - COUNT(DISTINCT REVIEW_ID)
        FROM FACT_REVIEWS
    """,

    "FACT_SHIPMENTS": """
        SELECT COUNT(*) - COUNT(DISTINCT SHIPMENT_ID)
        FROM FACT_SHIPMENTS
    """
}


for table, query in duplicate_queries.items():

    cur.execute(query)

    duplicates = cur.fetchone()[0]

    print(f"{table:20} : {duplicates}")


# ---------------------------------------------------------
# 3. NULL CHECK - FACT SALES
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("FACT_SALES NULL CHECK")
print("=" * 60)

cur.execute("""
SELECT
    COUNT(*) AS TOTAL_ROWS,
    COUNT_IF(ORDER_ITEM_ID IS NULL) AS NULL_ORDER_ITEM_ID,
    COUNT_IF(ORDER_ID IS NULL) AS NULL_ORDER_ID,
    COUNT_IF(CUSTOMER_ID IS NULL) AS NULL_CUSTOMER_ID,
    COUNT_IF(PRODUCT_ID IS NULL) AS NULL_PRODUCT_ID,
    COUNT_IF(ORDER_DATE IS NULL) AS NULL_ORDER_DATE,
    COUNT_IF(QUANTITY IS NULL) AS NULL_QUANTITY,
    COUNT_IF(UNIT_PRICE IS NULL) AS NULL_UNIT_PRICE,
    COUNT_IF(TOTAL_AMOUNT IS NULL) AS NULL_TOTAL_AMOUNT
FROM FACT_SALES
""")

result = cur.fetchone()

columns = [
    "TOTAL_ROWS",
    "NULL_ORDER_ITEM_ID",
    "NULL_ORDER_ID",
    "NULL_CUSTOMER_ID",
    "NULL_PRODUCT_ID",
    "NULL_ORDER_DATE",
    "NULL_QUANTITY",
    "NULL_UNIT_PRICE",
    "NULL_TOTAL_AMOUNT"
]

for column, value in zip(columns, result):
    print(f"{column:25} : {value:,}")


# ---------------------------------------------------------
# 4. FOREIGN KEY VALIDATION
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("FOREIGN KEY VALIDATION")
print("=" * 60)


fk_queries = {

    "FACT_SALES -> CUSTOMER": """
        SELECT COUNT(*)
        FROM FACT_SALES f
        LEFT JOIN DIM_CUSTOMER d
            ON f.CUSTOMER_ID = d.CUSTOMER_ID
        WHERE d.CUSTOMER_ID IS NULL
    """,

    "FACT_SALES -> PRODUCT": """
        SELECT COUNT(*)
        FROM FACT_SALES f
        LEFT JOIN DIM_PRODUCT d
            ON f.PRODUCT_ID = d.PRODUCT_ID
        WHERE d.PRODUCT_ID IS NULL
    """,

    "FACT_PAYMENTS -> ORDER": """
        SELECT COUNT(*)
        FROM FACT_PAYMENTS p
        LEFT JOIN FACT_SALES s
            ON p.ORDER_ID = s.ORDER_ID
        WHERE s.ORDER_ID IS NULL
    """,

    "FACT_REVIEWS -> CUSTOMER": """
        SELECT COUNT(*)
        FROM FACT_REVIEWS r
        LEFT JOIN DIM_CUSTOMER c
            ON r.CUSTOMER_ID = c.CUSTOMER_ID
        WHERE c.CUSTOMER_ID IS NULL
    """,

    "FACT_REVIEWS -> PRODUCT": """
        SELECT COUNT(*)
        FROM FACT_REVIEWS r
        LEFT JOIN DIM_PRODUCT p
            ON r.PRODUCT_ID = p.PRODUCT_ID
        WHERE p.PRODUCT_ID IS NULL
    """,

    "FACT_SHIPMENTS -> WAREHOUSE": """
        SELECT COUNT(*)
        FROM FACT_SHIPMENTS s
        LEFT JOIN DIM_WAREHOUSE w
            ON s.WAREHOUSE_ID = w.WAREHOUSE_ID
        WHERE w.WAREHOUSE_ID IS NULL
    """
}


for name, query in fk_queries.items():

    cur.execute(query)

    invalid = cur.fetchone()[0]

    print(f"{name:30} : {invalid:,}")


# ---------------------------------------------------------
# 5. FACT SALES BUSINESS VALIDATION
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("FACT SALES BUSINESS VALIDATION")
print("=" * 60)

cur.execute("""
SELECT COUNT(*)
FROM FACT_SALES
WHERE QUANTITY <= 0
   OR UNIT_PRICE < 0
   OR TOTAL_AMOUNT < 0
""")

invalid_sales = cur.fetchone()[0]

print("Invalid sales records :", invalid_sales)


# ---------------------------------------------------------
# 6. REVIEW VALIDATION
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("REVIEW VALIDATION")
print("=" * 60)

cur.execute("""
SELECT COUNT(*)
FROM FACT_REVIEWS
WHERE RATING < 1
   OR RATING > 5
""")

invalid_reviews = cur.fetchone()[0]

print("Invalid ratings :", invalid_reviews)


# ---------------------------------------------------------
# CLOSE
# ---------------------------------------------------------

cur.close()
conn.close()

print("\n" + "=" * 60)
print("VALIDATION COMPLETED")
print("=" * 60)