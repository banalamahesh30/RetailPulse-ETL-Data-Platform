import pandas as pd
from config.db_connection import get_connection

conn = get_connection()
query = "select * from Sellers"

Sellers_df = pd.read_sql_query( query, conn)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print (Sellers_df)

Sellers_df.to_csv("data/raw/Sellers.csv", index = False)
Sellers_df.to_parquet("data/raw/Sellers.parquet", index = False)

print("Orders Sellers Successfully")

conn.close()
