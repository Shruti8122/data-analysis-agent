from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

def run_automl(df):
    numeric = df.select_dtypes(include="number")

    if numeric.shape[1] < 2:
        return "Not enough numeric data for AutoML"

    X = numeric.iloc[:, :-1]
    y = numeric.iloc[:, -1]

    if y.nunique() < 10:
        model = RandomForestClassifier()
        task = "Classification"
    else:
        model = RandomForestRegressor()
        task = "Regression"

    model.fit(X, y)

    return f"{task} → Recommended model: {model.__class__.__name__}"
