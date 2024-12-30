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
        "legend.title_fontsize": 10,
        "figure.titlesize": 14,
        "lines.linewidth": 1.5,
        "lines.markersize": 6,
    }
)

FROM_YEAR = 2014
TO_YEAR = 2023
MONTHLY_DATASET_PATH = Path("monthly.csv")
YEARLY_DATASET_PATH = Path("final.csv")

MONTH_LABELS = (
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
)


class StationarityStats(NamedTuple):
    adf_stat: float
    adf_pval: float
    adf_lags: int
    kpss_stat: float
    kpss_pval: float
    kpss_lags: int


def lineplot(data: pd.DataFrame, y: str, ylabel: str):
    fig, ax = plt.subplots()
    sns.lineplot(data=data, x="Date", y=y, ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel(ylabel)
    ax.xaxis.set_minor_locator(NullLocator())
    for year in range(FROM_YEAR, TO_YEAR + 1):
        plt.axvline(
            pd.Timestamp(f"{year}-01-01"), color="black", linestyle="--", linewidth=0.8
        )

    return fig


def seasonal_plot(data: pd.DataFrame, y: str, ylabel: str):
    fig, ax = plt.subplots()
    sns.lineplot(data=data, x="month", y=y, hue="year", palette="bright")
    ax.set_xticks(range(1, len(MONTH_LABELS) + 1))
    ax.set_xticklabels(MONTH_LABELS, rotation=45)
    ax.set_xlabel("Month")
    ax.set_ylabel(ylabel)
    ax.xaxis.set_minor_locator(NullLocator())
    ax.legend(title="Year", bbox_to_anchor=(1.0, 1.0))

    return fig


def boxplot_yearly(data: pd.DataFrame, y: str, ylabel: str):
    fig, ax = plt.subplots()
    sns.boxplot(data=data, x="year", y=y, ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel(ylabel)
    ax.xaxis.set_minor_locator(NullLocator())

    return fig


def boxplot_monthly(data: pd.DataFrame, y: str, ylabel: str):
    fig, ax = plt.subplots()
    sns.boxplot(data=data, x="month", y=y, ax=ax)
    ax.set_xticks(range(len(MONTH_LABELS)))
    ax.set_xticklabels(MONTH_LABELS, rotation=45)
    ax.set_xlabel("Month")
    ax.set_ylabel(ylabel)
    ax.xaxis.set_minor_locator(NullLocator())

    return fig


def is_stationary(ts: pd.Series, alpha: float = 0.05, regression: str = "ct") -> bool:
    stats = stationarity_stats(ts, regression=regression)
    return stats.adf_pval <= alpha and stats.kpss_pval > alpha


def stationarity_stats(ts: pd.Series, regression: str = "ct") -> StationarityStats:
    adf_stat, adf_pval, adf_lags, *_ = adfuller(ts, regression=regression)
    kpss_stat, kpss_pval, kpss_lags, *_ = kpss(ts, regression=regression)

    return StationarityStats(
        adf_stat, adf_pval, adf_lags, kpss_stat, kpss_pval, kpss_lags
    )


def stationarity_table(
    ts: pd.Series, period: int = 12, regression: str = "ct"
) -> pd.DataFrame:
    ts_log = np.log(ts)
    tfmt = dict()
    tfmt["Orig"] = ts
    tfmt["Diff"] = ts.diff().dropna()
    tfmt["Season"] = ts.diff(period).dropna()
    tfmt["Diff + Season"] = ts.diff().diff(period).dropna()
    tfmt["Log"] = ts_log
    tfmt["Diff(Log)"] = ts_log.diff().dropna()
    tfmt["Season(Log)"] = ts_log.diff(period).dropna()
    tfmt["(Diff + Season)(Log)"] = ts_log.diff().diff(period).dropna()

    rows = []
    for name, tfmt_ts in tfmt.items():
        stats = stationarity_stats(tfmt_ts, regression=regression)
        row = {
            "Name": name,
            "ADF p-val": stats.adf_pval,
            "ADF lags": stats.adf_lags,
            "KPSS p-val": stats.kpss_pval,
            "KPSS lags": stats.kpss_lags,
            "Stationary": is_stationary(tfmt_ts, regression=regression),
        }
        rows.append(row)

    return pd.DataFrame(rows)


def get_montlhy_dataset() -> pd.DataFrame:
    df = pd.read_csv(MONTHLY_DATASET_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df["year"] = df["Date"].dt.year
    df["month"] = df["Date"].dt.month
    mask = (df.year >= FROM_YEAR) & (df.year <= TO_YEAR)

    return df[mask]


def get_yearly_dataset() -> pd.DataFrame:
    return pd.read_csv(YEARLY_DATASET_PATH)
