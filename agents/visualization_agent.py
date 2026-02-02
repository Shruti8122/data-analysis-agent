import seaborn as sns
import matplotlib.pyplot as plt

def generate_plots(df):
    plots = []

    for col in df.select_dtypes(include="number").columns:
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        ax.set_title(col)
        plots.append(fig)

    return plots
