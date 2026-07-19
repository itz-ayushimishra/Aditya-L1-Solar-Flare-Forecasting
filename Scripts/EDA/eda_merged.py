from pathlib import Path
import pandas as pd

# Path to merged data
project_root = Path(__file__).resolve().parents[2]
merged_path = project_root / "Processed_Data" / "MERGED"

print(merged_path)
print(merged_path.exists())

# Find all merged CSV files
files = list(merged_path.rglob("*_Merged.csv"))

print(f"Found {len(files)} merged files.\n")

for file in files:
    print("=" * 60)
    print(f"File: {file.name}")

    df = pd.read_csv(file)

    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nFirst 5 Rows:")
    print(df.head())
    print()

print(merged_path.resolve())
print(merged_path.exists())