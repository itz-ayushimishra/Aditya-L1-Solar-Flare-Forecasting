from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_FOLDER = PROJECT_ROOT / "Scripts"

sys.path.append(str(SCRIPTS_FOLDER))

import pandas as pd
from config import *

SOLEXS_FOLDER = PROCESSED_DATA / "SoLEXS"
HELIOS_FOLDER = PROCESSED_DATA / "HEL1OS"

OUTPUT_FOLDER = PROCESSED_DATA / "MERGED"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


def convert_solexs_time(df):
    df = df.copy()
    df["TIME"] = pd.to_datetime(df["TIME"], unit="s")
    return df


for date_folder in sorted(HELIOS_FOLDER.iterdir()):

    if not date_folder.is_dir():
        continue

    date = date_folder.name

    print("=" * 60)
    print(date)

    # ---------------- SoLEXS ----------------

    solexs_file = SOLEXS_FOLDER / date / "SDD2_LightCurve.csv"

    if not solexs_file.exists():
        print("SoLEXS LightCurve not found")
        continue

    solexs_df = pd.read_csv(solexs_file)

    solexs_df = convert_solexs_time(solexs_df)

    solexs_df = (
        solexs_df
        .dropna(subset=["COUNTS"])
        .sort_values("TIME")
        .reset_index(drop=True)
    )

    # Round timestamps
    solexs_df["TIME"] = (
    solexs_df["TIME"]
    .dt.round("s")
    .astype("datetime64[us]")
    )   

    # ---------------- HEL1OS ----------------

    for detector_folder in sorted(date_folder.iterdir()):

        if not detector_folder.is_dir():
            continue

        detector = detector_folder.name

        helios_files = list(detector_folder.glob("LightCurve*.csv"))

        if len(helios_files) == 0:
            continue

        helios_file = helios_files[0]

        helios_df = pd.read_csv(helios_file)

        helios_df["ISOT"] = pd.to_datetime(helios_df["ISOT"])

        helios_df = (
            helios_df
            .dropna(subset=["CTR"])
            .sort_values("ISOT")
            .reset_index(drop=True)
        )

        # Round timestamps
        helios_df["ISOT"] = (
            helios_df["ISOT"]
            .dt.round("s")
            .astype("datetime64[us]")
        )

        print(f"Merging {detector}")

        print("SoLEXS rows :", len(solexs_df))
        print("HEL1OS rows :", len(helios_df))

        print(solexs_df["TIME"].dtype)
        print(helios_df["ISOT"].dtype)

        merged = pd.merge_asof(
        helios_df.sort_values("ISOT"),
        solexs_df.sort_values("TIME"),
        left_on="ISOT",
        right_on="TIME",
        direction="nearest",
        tolerance=pd.Timedelta(seconds=1)
        )

        merged = merged.dropna(subset=["COUNTS"])

        print("Merged rows :", len(merged))
        print("Matched rows :", merged["COUNTS"].notna().sum())

        output_folder = OUTPUT_FOLDER / date / detector
        output_folder.mkdir(parents=True, exist_ok=True)

        output_file = output_folder / f"{detector}_Merged.csv"

        merged.to_csv(output_file, index=False)

        print("Saved ->", output_file)

print("\nFinished!")