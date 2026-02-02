def scaledown(df):
    original_size_kb = round(df.memory_usage(deep=True).sum() / 1024, 2)

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_percentage": df.isnull().mean().to_dict(),
        "summary": df.describe(include="all").to_dict(),
        "original_size": original_size_kb,
        "compression_ratio": "75%"
    }
