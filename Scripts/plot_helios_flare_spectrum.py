from pathlib import Path
import ast

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from config import *

PAYLOAD = "HEL1OS"

SUMMARY = PROCESSED_DATA / PAYLOAD / "LightCurve_Summary.csv"

PROCESSED_FOLDER = PROCESSED_DATA / PAYLOAD

PLOT_FOLDER = PLOTS / PAYLOAD / "FlareSpectrum"

PLOT_FOLDER.mkdir(parents=True, exist_ok=True)

summary = pd.read_csv(SUMMARY)

for _, flare in summary.iterrows():

    date = str(flare["DATE"])

    detector = flare["DETECTOR"]

    peak_time = pd.to_datetime(flare["PEAK_TIME"])

    spectrum_file = (
        PROCESSED_FOLDER /
        date /
        detector /
        f"{detector}_Spectrum.csv"
    )

    if not spectrum_file.exists():
        continue

    print(f"Processing {date} | {detector}")

    spec = pd.read_csv(spectrum_file)

    peak_seconds = (
        peak_time -
        peak_time.normalize()
    ).total_seconds()

    spec["DIFF"] = (
        spec["TSTART"] -
        peak_seconds
    ).abs()

    row = spec.loc[spec["DIFF"].idxmin()]

    channels = np.array(
        ast.literal_eval(row["CHANNEL"])
    )

    counts = np.array(
        ast.literal_eval(row["COUNTS"]),
        dtype=float
    )

    plt.figure(figsize=(10,5))

    plt.plot(channels, counts)

    plt.xlabel("Channel")
    plt.ylabel("Counts")

    plt.title(
        f"{date} | {detector}"
    )

    detector_plot_folder = (
    PLOT_FOLDER /
    date /
    detector
    )

    detector_plot_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    output = (
    detector_plot_folder /
    f"{date}_{detector}_FlareSpectrum.png"
    )
    plt.savefig(output,dpi=300)

    plt.close()

    print("Saved ->", output)

print("\nDone!")