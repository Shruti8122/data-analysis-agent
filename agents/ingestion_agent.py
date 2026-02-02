import pandas as pd
import io

def load_csv(file_bytes):
    return pd.read_csv(io.BytesIO(file_bytes))
