def scaledown(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_percentage": df.isnull().mean().to_dict(),
        "summary": df.describe().to_dict()
    }