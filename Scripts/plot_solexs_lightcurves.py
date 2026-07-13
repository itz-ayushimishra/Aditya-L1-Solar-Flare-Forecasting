from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from config import *

PAYLOAD = "SoLEXS"

PROCESSED_FOLDER = PROCESSED_DATA / PAYLOAD
PLOTS_FOLDER = PLOTS / PAYLOAD / "LightCurve"

PLOTS_FOLDER.mkdir(parents=True, exist_ok=True)

# Get all date folders
date_folders = sorted(PROCESSED_FOLDER.iterdir())

for folder in date_folders:

    if not folder.is_dir():
        continue

    lightcurve_file = folder / "SDD2_LightCurve.csv"

    if not lightcurve_file.exists():
        print(f"Skipping {folder.name} (No Light Curve)")
        continue

    print("=" * 50)
    print("Date:", folder.name)

    # Read CSV
    df = pd.read_csv(lightcurve_file)

    # Remove missing values
    df = df.dropna(subset=["COUNTS"])

    if df.empty:
        print("No valid data.")
        continue

    # Basic statistics
    print(df["COUNTS"].describe())

    # Maximum count
    max_row = df.loc[df["COUNTS"].idxmax()]

    print("\nMaximum Counts:")
    print(max_row)

    # Plot
    plt.figure(figsize=(12,5))

    df["TIME"] = pd.to_datetime(df["TIME"], unit="s")

    plt.plot(df["TIME"], df["COUNTS"])
    plt.gcf().autofmt_xdate()

    plt.title(f"Light Curve - {folder.name}")
    plt.xlabel("TIME")
    plt.ylabel("COUNTS")

    plt.grid(True)

    # Save graph
    plot_file = PLOTS_FOLDER / f"{folder.name}_LightCurve.png"
    plt.savefig(plot_file, dpi=300)
    plt.close()

    print(f"Graph saved: {plot_file}")

print("\nAll Light Curves processed successfully!")