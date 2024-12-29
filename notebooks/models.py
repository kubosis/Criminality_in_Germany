from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

MONTHLY_DATASET_PATH = Path("monthly.csv")
YEARLY_DATASET_PATH = Path("final.csv")

plt.style.use("ggplot")


def total_offences_lineplot(data: pd.DataFrame):
    fig, ax = plt.subplots()
    sns.lineplot(data=data, x="Date", y="Total offences", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Offences")

    return fig


def total_offences_boxplot(data: pd.DataFrame):
    fig, ax = plt.subplots()
    sns.boxplot(data=data, x="year", y="Total offences", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Offences")

    return fig


def get_montlhy_dataset():
    df = pd.read_csv(MONTHLY_DATASET_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df["year"] = df["Date"].dt.year
    df["month"] = df["Date"].dt.month
    mask = (df.year >= 2014) & (df.year <= 2023)

    return df[mask]


def get_yearly_dataset():
    return pd.read_csv(YEARLY_DATASET_PATH)
