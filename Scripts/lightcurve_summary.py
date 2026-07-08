from pathlib import Path
import pandas as pd

from config import *

PAYLOAD = "SoLEXS"

processed_folder = PROCESSED_DATA / PAYLOAD

summary = []

for folder in sorted(processed_folder.iterdir()):

    if not folder.is_dir():
        continue

    lightcurve_file = folder / "SDD2_LightCurve.csv"

    if not lightcurve_file.exists():
        continue

    print(f"Processing {folder.name}")

    df = pd.read_csv(lightcurve_file)

    # Remove missing values
    df = df.dropna(subset=["COUNTS"])

    if df.empty:
        continue

    max_row = df.loc[df["COUNTS"].idxmax()]

    background = df["COUNTS"].median()
    maximum = df["COUNTS"].max()
    std = df["COUNTS"].std()

    # Avoid division by zero
    if std == 0:
        significance = 0
    else:
        significance = (maximum - background) / std

    summary.append({
        "DATE": folder.name,
        "OBSERVATIONS": len(df),

        "MEAN_COUNTS": df["COUNTS"].mean(),
        "MEDIAN_COUNTS": background,
        "STD_COUNTS": df["COUNTS"].std(),

        "MIN_COUNTS": df["COUNTS"].min(),
        "MAX_COUNTS": maximum,

        "BACKGROUND_COUNTS": background,
        "FLARE_STRENGTH": maximum - background,
        "FLARE_SIGNIFICANCE": significance,

        "PEAK_TIME": max_row["TIME"]
    })

summary_df = pd.DataFrame(summary)

summary_file = processed_folder / "LightCurve_Summary.csv"

summary_df.to_csv(summary_file, index=False)

print("\nDone!")
print(summary_df)

print(f"\nSummary saved as {summary_file}")