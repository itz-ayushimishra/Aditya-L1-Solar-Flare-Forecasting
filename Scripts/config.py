from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Supported payloads
PAYLOADS = [
    "SoLEXS",
    "HEL1OS"
]

# Folder paths
RAW_DATA = PROJECT_ROOT / "Raw_Data"
PROCESSED_DATA = PROJECT_ROOT / "Processed_Data"
PLOTS = PROJECT_ROOT / "Plots"