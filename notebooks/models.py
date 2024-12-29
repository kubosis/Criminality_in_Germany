from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

MONTHLY_DATASET_PATH = Path("monthly.csv")
YEARLY_DATASET_PATH = Path("final.csv")

plt.style.use("ggplot")


def total_offences_plot(data: pd.DataFrame):
    fig, ax = plt.subplots()
    sns.lineplot(data=data, x="Date", y="Total offences", ax=ax)

    return fig


def get_montlhy_dataset():
    df = pd.read_csv(MONTHLY_DATASET_PATH)
    df["Date"] = pd.to_datetime(df["Date"])

    return df
