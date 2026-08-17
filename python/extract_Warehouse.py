import pandas as pd
from config.db_connection import get_connection

conn = get_connection()
query = "select * from Warehouses"

Warehouse_df = pd.read_sql_query( query, conn)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print (Warehouse_df)

Warehouse_df.to_csv("data/raw/Warehouse.csv", index = False)
Warehouse_df.to_parquet("data/raw/Warehouse.parquet", index = False)

print("Warehouse Exported Successfully")

conn.close()
