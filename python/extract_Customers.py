import pandas as pd

from config.db_connection import get_mysql_connection
from config.settings import RAW_DATA_DIR


def extract_customers():
    """Extract customer data from MySQL and save it as CSV and Parquet."""

    conn = None

    try:
        conn = get_mysql_connection()

        if conn is None:
            raise ConnectionError("Unable to connect to MySQL.")

        query = "SELECT * FROM Customers"

        customers_df = pd.read_sql_query(query, conn)

        # Save extracted data
        customers_df.to_csv(
            RAW_DATA_DIR / "customers.csv",
            index=False
        )

        customers_df.to_parquet(
            RAW_DATA_DIR / "customers.parquet",
            index=False
        )

        print(
            f"Customers extracted successfully: "
            f"{len(customers_df):,} records"
        )

        return customers_df

    except Exception as e:
        print(f"Customer extraction failed: {e}")
        raise

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    extract_customers()
