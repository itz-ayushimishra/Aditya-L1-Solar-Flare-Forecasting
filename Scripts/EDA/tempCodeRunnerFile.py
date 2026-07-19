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

top20.to_csv(
    report_folder / "top20_peak_events.csv",
    index=False
)