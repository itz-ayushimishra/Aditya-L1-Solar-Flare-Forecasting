from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent

processed_folder = PROJECT_ROOT / "Processed_Data" / "HEL1OS"
plots_folder = PROJECT_ROOT / "Plots" / "HEL1OS" / "LightCurve"

plots_folder.mkdir(parents=True, exist_ok=True)

for date_folder in sorted(processed_folder.iterdir()):

    if not date_folder.is_dir():
        continue

    for detector_folder in sorted(date_folder.iterdir()):

        if not detector_folder.is_dir():
            continue

        detector_plot_folder = (
            plots_folder /
            date_folder.name /
            detector_folder.name
        )

        detector_plot_folder.mkdir(parents=True, exist_ok=True)

        for csv_file in detector_folder.glob("LightCurve*.csv"):

            print(f"Processing {csv_file.name}")

            df = pd.read_csv(csv_file)

            if df.empty:
                continue

            df = df.dropna(subset=["CTR"])

            if df.empty:
                continue

            df["ISOT"] = pd.to_datetime(df["ISOT"])

            plt.figure(figsize=(12,5))

            plt.plot(df["ISOT"], df["CTR"])

            plt.title(csv_file.stem)
            plt.xlabel("Time")
            plt.ylabel("Count Rate (cts/sec)")
            plt.grid(True)

            plt.gcf().autofmt_xdate()

            output = detector_plot_folder / (csv_file.stem + ".png")

            plt.savefig(output, dpi=300)
            plt.close()

            print("Saved ->", output)

print("\nFinished plotting HEL1OS.")