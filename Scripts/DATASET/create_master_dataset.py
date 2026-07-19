from pathlib import Path
import pandas as pd

# Project Root
project_root = Path(__file__).resolve().parents[2]

# Paths
merged_path = project_root / "Processed_Data" / "MERGED"
output_path = project_root / "Processed_Data" / "MASTER_DATASET"

output_path.mkdir(exist_ok=True)

master_df = []

# Find every merged csv
files = list(merged_path.rglob("*_Merged.csv"))

print(f"Found {len(files)} merged files.\n")

for file in files:

    # Read csv
    df = pd.read_csv(file)

    # Detector name (CdTe1, CdTe2, CZT1, CZT2)
    detector = file.parent.name

    # Date (20260623 ...)
    date = file.parent.parent.name

    # Add new columns
    df["Detector"] = detector
    df["Date"] = date

    master_df.append(df)

# Combine everything
master_df = pd.concat(master_df, ignore_index=True)

# Sort by timestamp
master_df = master_df.sort_values("ISOT")

# Save
save_file = output_path / "Master_Dataset.csv"

master_df.to_csv(save_file, index=False)

print("=" * 50)
print("Master Dataset Created Successfully!")
print(f"Rows    : {master_df.shape[0]}")
print(f"Columns : {master_df.shape[1]}")
print(f"Saved at: {save_file}")