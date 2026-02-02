import pandas as pd
from io import BytesIO

def load_csv(file_bytes):
    return pd.read_csv(BytesIO(file_bytes))