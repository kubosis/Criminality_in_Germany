from pathlib import Path
from typing import NamedTuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scienceplots
import seaborn as sns
from matplotlib.ticker import NullLocator
from statsmodels.tsa.stattools import adfuller, kpss

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


class StationarityStats(NamedTuple):
    adf_stat: float
    adf_pval: float
    kpss_stat: float
    kpss_pval: float


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


def is_stationary(ts: pd.Series, alpha: float = 0.05, regression: str = "ct") -> bool:
    stats = stationarity_stats(ts, regression=regression)
    return stats.adf_pval <= alpha and stats.kpss_pval > alpha


def stationarity_stats(ts: pd.Series, regression: str = "ct") -> StationarityStats:
    adf_stat, adf_pval, *_ = adfuller(ts, regression=regression)
    kpss_stat, kpss_pval, *_ = kpss(ts, regression=regression)

    return StationarityStats(adf_stat, adf_pval, kpss_stat, kpss_pval)


def stationarity_table(
    ts: pd.Series, period: int = 12, regression: str = "ct"
) -> pd.DataFrame:
    ts_log = np.log(ts)
    tfmt = dict()
    tfmt["Orig"] = ts
    tfmt["Diff"] = ts.diff().dropna()
    tfmt["SeasonDiff"] = ts.diff(period).dropna()
    tfmt["Diff + SeasonDiff"] = ts.diff().diff(period).dropna()
    tfmt["Log"] = ts_log
    tfmt["Diff(Log)"] = ts_log.diff().dropna()
    tfmt["SeasonDiff(Log)"] = ts_log.diff(period).dropna()
    tfmt["(Diff + SeasonDiff)(Log)"] = ts_log.diff().diff(period).dropna()

    rows = []
    for name, tfmt_ts in tfmt.items():
        stats = stationarity_stats(tfmt_ts, regression=regression)
        row = {
            "Name": name,
            "ADF stat": stats.adf_stat,
            "ADF p-val": stats.adf_pval,
            "KPSS stat": stats.kpss_stat,
            "KPSS p-val": stats.kpss_pval,
            "Stationary": is_stationary(tfmt_ts, regression=regression),
        }
        rows.append(row)

    return pd.DataFrame(rows)


def get_montlhy_dataset() -> pd.DataFrame:
    df = pd.read_csv(MONTHLY_DATASET_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df["year"] = df["Date"].dt.year
    df["month"] = df["Date"].dt.month
    mask = (df.year >= 2014) & (df.year <= 2023)

    return df[mask]


def get_yearly_dataset() -> pd.DataFrame:
    return pd.read_csv(YEARLY_DATASET_PATH)