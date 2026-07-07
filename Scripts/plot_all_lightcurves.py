from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Folder containing processed data
processed_folder = Path("Processed_Data")

# Folder to save plots
plots_folder = Path("Plots")
plots_folder.mkdir(exist_ok=True)

# Get all date folders
date_folders = sorted(processed_folder.iterdir())

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
    plot_file = plots_folder / f"{folder.name}_LightCurve.png"
    plt.savefig(plot_file, dpi=300)
    plt.close()

    print(f"Graph saved: {plot_file}")

print("\nAll Light Curves processed successfully!")