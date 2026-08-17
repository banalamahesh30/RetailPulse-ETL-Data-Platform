import pandas as pd
from config.db_connection import get_connection

conn = get_connection()
query = "select * from Order_Items"

Orders_items_df = pd.read_sql_query( query, conn)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print (Orders_items_df)

Orders_items_df.to_csv("data/raw/Orders_items.csv", index = False)
Orders_items_df.to_parquet("data/raw/Orders_items.parquet", index = False)

print("Orders_items Exported Successfully")

conn.close()
