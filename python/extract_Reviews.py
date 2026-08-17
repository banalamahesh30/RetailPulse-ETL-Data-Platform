import pandas as pd
from config.db_connection import get_connection

conn = get_connection()
query = "select * from Reviews"

Reviews_df = pd.read_sql_query( query, conn)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print (Reviews_df)

Reviews_df.to_csv("data/raw/Reviews.csv", index = False)
Reviews_df.to_parquet("data/raw/Reviews.parquet", index = False)

print("Reviews Exported Successfully")

conn.close()
