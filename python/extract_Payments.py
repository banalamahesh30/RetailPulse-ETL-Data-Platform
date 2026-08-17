import pandas as pd
from config.db_connection import get_connection

conn = get_connection()
query = "select * from Payments"
Payments_df = pd.read_sql_query( query, conn)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print (Payments_df)

Payments_df.to_csv("data/raw/Payments.csv", index = False)
Payments_df.to_parquet("data/raw/Payments.parquet", index = False)

print("Payments exported Successfully")

conn.close()
