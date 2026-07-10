from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast

from config import *

PAYLOAD = "SoLEXS"

SUMMARY = PROCESSED_DATA / PAYLOAD / "LightCurve_Summary.csv"
PROCESSED_FOLDER = PROCESSED_DATA / PAYLOAD
PLOT_FOLDER = PLOTS / PAYLOAD / "FlareSpectrum"

PLOT_FOLDER.mkdir(parents=True, exist_ok=True)

summary = pd.read_csv(SUMMARY)

for _, flare in summary.iterrows():

    # ---------- FIX DATE ----------
    date = str(int(flare["DATE"]))

    detector = "SDD2"
    peak_time = float(flare["PEAK_TIME"])

    spectrum_file = PROCESSED_FOLDER / date / f"{detector}_Spectrum.csv"

    print(spectrum_file)

    if not spectrum_file.exists():
        print("Spectrum file not found\n")
        continue

    spec = pd.read_csv(spectrum_file)

    # Find nearest spectrum
    spec["DIFF"] = (spec["TSTART"] - peak_time).abs()
    row = spec.loc[spec["DIFF"].idxmin()]

    # Convert lists
    channels = np.array(ast.literal_eval(row["CHANNEL"]))

    counts = np.array(
        eval(
            row["COUNTS"].replace("nan", "np.nan"),
            {"np": np}
        ),
        dtype=float
    )

    plt.figure(figsize=(10,5))
    plt.plot(channels, counts)

    plt.xlabel("Channel")
    plt.ylabel("Counts")
    plt.title(f"{date} | {detector}")

    output = PLOT_FOLDER / f"{date}_{detector}.png"

    plt.savefig(output)
    plt.close()

    print(f"Saved -> {output}")

print("\nDone!")