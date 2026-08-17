import pandas as pd
from config.db_connection import get_connection

conn = get_connection()
query = "select * from Orders"

Orders_df = pd.read_sql_query( query, conn)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print (Orders_df)

Orders_df.to_csv("data/raw/Orders.csv", index = False)
Orders_df.to_parquet("data/raw/Orders.parquet", index = False)

print("Orders Exported Successfully")

conn.close()
