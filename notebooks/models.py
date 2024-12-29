from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import scienceplots
import seaborn as sns
from matplotlib.ticker import NullLocator

plt.style.use(["science", "notebook"])
plt.rcParams.update(
    {
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.titlesize": 14,
        "lines.linewidth": 1.5,
        "lines.markersize": 6,
    }
)

MONTHLY_DATASET_PATH = Path("monthly.csv")
YEARLY_DATASET_PATH = Path("final.csv")


def total_offences_lineplot(data: pd.DataFrame):
    fig, ax = plt.subplots()
    sns.lineplot(data=data, x="Date", y="Total offences", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Offences")
    ax.xaxis.set_minor_locator(NullLocator())

    return fig


def total_offences_boxplot_yearly(data: pd.DataFrame):
    fig, ax = plt.subplots()
    sns.boxplot(data=data, x="year", y="Total offences", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Offences")
    ax.xaxis.set_minor_locator(NullLocator())

    return fig


def total_offences_boxplot_monthly(data: pd.DataFrame):
    fig, ax = plt.subplots()
    sns.boxplot(data=data, x="month", y="Total offences", ax=ax)
    ax.set_xticklabels(
        [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
    )
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Offences")
    ax.xaxis.set_minor_locator(NullLocator())

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
