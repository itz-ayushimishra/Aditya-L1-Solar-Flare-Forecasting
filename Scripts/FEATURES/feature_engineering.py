from pathlib import Path
import pandas as pd
import numpy as np

# ----------------------------
# Project Paths
# ----------------------------
project_root = Path(__file__).resolve().parents[2]

input_file = (
    project_root
    / "Processed_Data"
    / "MASTER_DATASET"
    / "Master_Dataset.csv"
)

output_folder = (
    project_root
    / "Processed_Data"
    / "FEATURE_DATASET"
)

output_folder.mkdir(exist_ok=True)

output_file = output_folder / "Feature_Dataset.csv"

# ----------------------------
# Read Dataset
# ----------------------------
print("Reading Master Dataset...")

df = pd.read_csv(input_file)

print(f"Rows : {len(df)}")

# ----------------------------
# Sort Data
# ----------------------------
df["ISOT"] = pd.to_datetime(df["ISOT"])

df = df.sort_values(["Date", "Detector", "ISOT"])

# ----------------------------
# Feature Engineering
# ----------------------------
print("Creating Features...")

group = df.groupby(["Date", "Detector"])

# --------------------------------------------------
# Difference
# --------------------------------------------------

df["COUNTS_DIFF"] = group["COUNTS"].diff()
df["CTR_DIFF"] = group["CTR"].diff()

# --------------------------------------------------
# Percent Change
# --------------------------------------------------

df["COUNTS_PERCENT_CHANGE"] = group["COUNTS"].pct_change()
df["CTR_PERCENT_CHANGE"] = group["CTR"].pct_change()

# --------------------------------------------------
# Rolling Features
# --------------------------------------------------

for window in [3, 5, 10, 30]:

    df[f"COUNTS_MEAN_{window}"] = (
        group["COUNTS"]
        .transform(lambda x: x.rolling(window, min_periods=1).mean())
    )

    df[f"CTR_MEAN_{window}"] = (
        group["CTR"]
        .transform(lambda x: x.rolling(window, min_periods=1).mean())
    )

    df[f"COUNTS_STD_{window}"] = (
        group["COUNTS"]
        .transform(lambda x: x.rolling(window, min_periods=1).std())
    )

    df[f"CTR_STD_{window}"] = (
        group["CTR"]
        .transform(lambda x: x.rolling(window, min_periods=1).std())
    )

    df[f"COUNTS_MAX_{window}"] = (
        group["COUNTS"]
        .transform(lambda x: x.rolling(window, min_periods=1).max())
    )

    df[f"CTR_MAX_{window}"] = (
        group["CTR"]
        .transform(lambda x: x.rolling(window, min_periods=1).max())
    )

    df[f"COUNTS_MIN_{window}"] = (
        group["COUNTS"]
        .transform(lambda x: x.rolling(window, min_periods=1).min())
    )

    df[f"CTR_MIN_{window}"] = (
        group["CTR"]
        .transform(lambda x: x.rolling(window, min_periods=1).min())
    )

# --------------------------------------------------
# EMA
# --------------------------------------------------

for span in [5, 10, 30]:

    df[f"COUNTS_EMA_{span}"] = (
        group["COUNTS"]
        .transform(lambda x: x.ewm(span=span, adjust=False).mean())
    )

    df[f"CTR_EMA_{span}"] = (
        group["CTR"]
        .transform(lambda x: x.ewm(span=span, adjust=False).mean())
    )

# --------------------------------------------------
# Mathematical Features
# --------------------------------------------------

df["COUNTS_SQUARED"] = df["COUNTS"] ** 2
df["CTR_SQUARED"] = df["CTR"] ** 2

import numpy as np

df["LOG_COUNTS"] = np.log1p(df["COUNTS"])
df["LOG_CTR"] = np.log1p(df["CTR"])

# --------------------------------------------------
# Z Score
# --------------------------------------------------

df["COUNTS_ZSCORE"] = (
    (df["COUNTS"] - df["COUNTS"].mean())
    /
    (df["COUNTS"].std() + 1e-8)
)

df["CTR_ZSCORE"] = (
    (df["CTR"] - df["CTR"].mean())
    /
    (df["CTR"].std() + 1e-8)
)

# --------------------------------------------------
# Signal-to-Noise Ratio
# --------------------------------------------------

df["COUNTS_SNR"] = (
    (df["COUNTS"] - df["COUNTS_MEAN_30"])
    /
    (df["COUNTS_STD_30"] + 1e-8)
)

df["CTR_SNR"] = (
    (df["CTR"] - df["CTR_MEAN_30"])
    /
    (df["CTR_STD_30"] + 1e-8)
)

# --------------------------------------------------
# Relative Change (5 sec)
# --------------------------------------------------

df["COUNTS_REL_CHANGE_5"] = (
    group["COUNTS"].diff(5)
)

df["CTR_REL_CHANGE_5"] = (
    group["CTR"].diff(5)
)

# --------------------------------------------------
# Time Features
# --------------------------------------------------

df["Hour"] = df["ISOT"].dt.hour
df["Minute"] = df["ISOT"].dt.minute
df["Second"] = df["ISOT"].dt.second

# --------------------------------------------------
# Detector Encoding
# --------------------------------------------------

df["Detector_ID"] = (
    df["Detector"]
    .astype("category")
    .cat.codes
)

# --------------------------------------------------
# Flare Candidate
# --------------------------------------------------

df["FLARE_CANDIDATE"] = (
    (df["COUNTS_SNR"] > 3)
    &
    (df["COUNTS_DIFF"] > 0)
).astype(int)

# --------------------------------------------------
# Replace NaN
# -------------------------------------------------- 

df.fillna(0, inplace=True)

# ----------------------------
# Save
# ----------------------------
df.to_csv(output_file, index=False)

print("=" * 50)
print("Feature Dataset Created Successfully!")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")
print(f"Saved at: {output_file}")