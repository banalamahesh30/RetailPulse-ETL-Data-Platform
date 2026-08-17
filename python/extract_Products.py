import pandas as pd
from config.db_connection import get_connection

conn = get_connection()
query = "select * from Products"

Products_df = pd.read_sql_query( query, conn)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print (Products_df)

Products_df.to_csv("data/raw/Products.csv", index = False)
Products_df.to_parquet("data/raw/Products.parquet", index = False)

print("Products Exported Successfully")

conn.close()
