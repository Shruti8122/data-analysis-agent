import pandas as pd
from io import BytesIO
from sqlalchemy import create_engine

def load_data(file_bytes=None, file_name=None, sql_url=None, table=None):
    # CSV
    if file_name and file_name.endswith(".csv"):
        return pd.read_csv(BytesIO(file_bytes))

    # Parquet
    if file_name and file_name.endswith(".parquet"):
        return pd.read_parquet(BytesIO(file_bytes))

    # SQL Database
    if sql_url and table:
        engine = create_engine(sql_url)
        return pd.read_sql_table(table, engine)

    raise ValueError("Unsupported data source")
