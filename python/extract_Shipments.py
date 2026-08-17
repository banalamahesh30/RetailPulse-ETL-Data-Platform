import pandas as pd
from config.db_connection import get_connection

conn = get_connection()
query = "select * from Shipments"
Shipments_df = pd.read_sql_query( query, conn)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print (Shipments_df)

Shipments_df.to_csv("data/raw/Shipments.csv", index = False)
Shipments_df.to_parquet("data/raw/Shipments.parquet", index = False)

print("Shipments exported Successfully")

conn.close()
