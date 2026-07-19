from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

project_root = Path(__file__).resolve().parents[2]

input_file = (
    project_root
    / "Processed_Data"
    / "FEATURE_DATASET"
    / "Feature_Dataset.csv"
)

report_folder = (
    project_root
    / "EDA_REPORT"
)

report_folder.mkdir(exist_ok=True)

print("Reading Feature Dataset...")

df = pd.read_csv(input_file)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# Sample for plotting (keeps plots fast)
sample_df = df.sample(
    n=min(100000, len(df)),
    random_state=42
)

print("Creating Summary Report...")

summary_file = report_folder / "summary.txt"

with open(summary_file, "w") as f:

    f.write("=" * 60 + "\n")
    f.write("ADITYA-L1 SOLAR FLARE PROJECT\n")
    f.write("EDA REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Generated On : {datetime.now()}\n\n")

    f.write(f"Rows          : {df.shape[0]}\n")
    f.write(f"Columns       : {df.shape[1]}\n\n")

    f.write(f"Date Range\n")
    f.write(f"{df['Date'].min()}  -->  {df['Date'].max()}\n\n")

    f.write(f"Detectors\n")
    f.write(f"{df['Detector'].unique()}\n\n")

    f.write("Missing Values\n")
    f.write(str(df.isnull().sum()))

print("Detector Statistics...")

detector_stats = (
    df.groupby("Detector")
      .agg({
          "COUNTS": ["mean", "max", "min", "std"],
          "CTR": ["mean", "max", "min", "std"]
      })
)

detector_stats.to_csv(
    report_folder / "detector_statistics.csv"
)

print("Daily Statistics...")

daily_stats = (
    df.groupby("Date")
      .agg({
          "COUNTS": ["mean", "max"],
          "CTR": ["mean", "max"]
      })
)

daily_stats.to_csv(
    report_folder / "daily_statistics.csv"
)

print("Finding Peak Events...")

print("Plotting COUNTS Histogram...")

plt.figure(figsize=(10,5))

sns.histplot(
    sample_df["COUNTS"],
    bins=100,
    kde=True
)

plt.title("Distribution of COUNTS")
plt.tight_layout()

plt.savefig(report_folder/"counts_histogram.png")

plt.close()

print("Plotting CTR Histogram...")

plt.figure(figsize=(10,5))

sns.histplot(
    sample_df["CTR"],
    bins=100,
    kde=True
)

plt.title("Distribution of CTR")

plt.tight_layout()

plt.savefig(report_folder/"ctr_histogram.png")

plt.close()

print("Correlation Matrix...")

corr_columns = [
    "COUNTS",
    "CTR",
    "COUNTS_DIFF",
    "CTR_DIFF",
    "COUNTS_MEAN_5",
    "CTR_MEAN_5",
    "COUNTS_STD_5",
    "CTR_STD_5",
]

corr = sample_df[corr_columns].corr()

plt.figure(figsize=(9,7))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm"
)

plt.tight_layout()

plt.savefig(report_folder/"correlation_heatmap.png")

plt.close()

print("Detector Boxplot...")

plt.figure(figsize=(12,6))

sns.boxplot(
    x="Detector",
    y="COUNTS",
    data=sample_df
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(report_folder/"detector_boxplot.png")

plt.close()

print("Daily Trend...")

daily_mean = (
    df.groupby("Date")["COUNTS"]
      .mean()
)

plt.figure(figsize=(12,5))

daily_mean.plot()

plt.ylabel("Mean Counts")

plt.tight_layout()

plt.savefig(report_folder/"daily_counts.png")

plt.close()

daily_ctr = (
    df.groupby("Date")["CTR"]
      .mean()
)

plt.figure(figsize=(12,5))

daily_ctr.plot()

plt.ylabel("Mean CTR")

plt.tight_layout()

plt.savefig(report_folder/"daily_ctr.png")

plt.close()

print("Scatter Plot...")

plt.figure(figsize=(8,6))

sns.scatterplot(
    x="COUNTS",
    y="CTR",
    data=sample_df,
    s=8
)

plt.tight_layout()

plt.savefig(report_folder/"counts_vs_ctr.png")

plt.close()

print("Detector Distribution...")

plt.figure(figsize=(8,5))

sample_df["Detector"].value_counts().plot.bar()

plt.tight_layout()

plt.savefig(report_folder/"detector_distribution.png")

plt.close()

top20 = (
    df.nlargest(20, "COUNTS")[
        [
            "Date",
            "Detector",
            "ISOT",
            "COUNTS",
            "CTR"
        ]
    ]
)

print("Peak Event Distribution...")

plt.figure(figsize=(10,5))

top20["COUNTS"].plot.bar()

plt.tight_layout()

plt.savefig(report_folder/"peak_events_distribution.png")

plt.close()

print("Sample Time Series...")

sample_day = df["Date"].iloc[0]

plot_df = df[df["Date"] == sample_day].head(3000)

plt.figure(figsize=(14,5))

plt.plot(plot_df["COUNTS"])

plt.ylabel("Counts")

plt.title(f"Sample Time Series ({sample_day})")

plt.tight_layout()

plt.savefig(report_folder/"sample_timeseries.png")

plt.close()

top20.to_csv(
    report_folder / "top20_peak_events.csv",
    index=False
)

print("="*60)
print("Professional EDA Report Generated Successfully!")
print(report_folder)