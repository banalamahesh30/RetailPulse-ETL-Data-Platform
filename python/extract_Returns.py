import pandas as pd
from config.db_connection import get_connection

conn = get_connection()
query = "select * from Returns"

Returns_df = pd.read_sql_query( query, conn)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print (Returns_df)

Returns_df.to_csv("data/raw/Returns.csv", index = False)
Returns_df.to_parquet("data/raw/Returns.parquet", index = False)

print("Returns Exported Successfully")

conn.close()
