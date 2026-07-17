from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

processed_folder = PROJECT_ROOT / "Processed_Data" / "HEL1OS"

summary = []

for date_folder in sorted(processed_folder.iterdir()):

    if not date_folder.is_dir():
        continue

    for detector_folder in sorted(date_folder.iterdir()):

        if not detector_folder.is_dir():
            continue

        detector = detector_folder.name

        for csv_file in sorted(detector_folder.glob("LightCurve*.csv")):

            print(f"Processing {date_folder.name} | {detector} | {csv_file.name}")

            df = pd.read_csv(csv_file)

            df = df.dropna(subset=["CTR"])

            if df.empty:
                continue

            maximum = df["CTR"].max()
            background = df["CTR"].median()
            std = df["CTR"].std()

            if std == 0:
                significance = 0
            else:
                significance = (maximum - background) / std

            max_row = df.loc[df["CTR"].idxmax()]

            summary.append({
                "DATE": date_folder.name,
                "DETECTOR": detector,
                "ENERGY_BAND": csv_file.stem.replace("LightCurve_", ""),

                "OBSERVATIONS": len(df),

                "MEAN_COUNTS": df["CTR"].mean(),
                "MEDIAN_COUNTS": background,
                "STD_COUNTS": std,

                "MIN_COUNTS": df["CTR"].min(),
                "MAX_COUNTS": maximum,

                "BACKGROUND_COUNTS": background,
                "FLARE_STRENGTH": maximum - background,
                "FLARE_SIGNIFICANCE": significance,

                "PEAK_TIME": max_row["ISOT"]
            })

summary_df = pd.DataFrame(summary)

summary_file = processed_folder / "LightCurve_Summary.csv"

summary_df.to_csv(summary_file, index=False)

print("\nDone!")
print(summary_df)

print(f"\nSummary saved as {summary_file}")