#  Aditya-L1 Solar Flare Forecasting & Nowcasting

**Project Status:** Under Active Development

## Overview

This project focuses on forecasting and nowcasting solar flares using observations from the **SoLEXS (Solar Low Energy X-ray Spectrometer)** instrument onboard **ISRO's Aditya-L1 mission**.

The goal is to process raw satellite observations, extract meaningful scientific features, and build machine learning models capable of predicting solar flare activity.

---

## Project Objectives

- Read SoLEXS FITS files
- Extract Light Curves
- Extract Spectra
- Extract GTI information
- Generate daily plots
- Detect solar flares
- Engineer scientific features
- Build forecasting models
- Build nowcasting models

---

## Dataset

The observational data used in this project is obtained from the **ISRO PRADAN Portal**.

Mission:
- Aditya-L1

Instrument:
- SoLEXS (Solar Low Energy X-ray Spectrometer)

Observation Period (Current):
- 02 June 2026 – 03 July 2026

Data Products:
- Light Curves
- Spectra
- Good Time Intervals (GTI)

---

## Project Structure

```
Aditya_L1_Project/
│
├── Scripts/
│   ├── main.py
│   ├── plot_all_lightcurves.py
│   ├── lightcurve_summary.py
│   ├── spectrum.py
│   ├── gti.py
│   ├── lightcurve.py
│   └── utils.py
│
├── Raw_Data/
│
├── Processed_Data/
│
├── Plots/
│
├── LightCurve_Summary.csv
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

---

## Current Progress

✅ FITS extraction
✅ CSV conversion
✅ Light curve generation
✅ Daily statistical analysis
⬜ Flare detection
⬜ Feature engineering
⬜ Spectrum analysis
⬜ Machine learning models

---

## Technologies Used

- Python
- Astropy
- Pandas
- NumPy
- Matplotlib
- Git
- GitHub

---

## Future Work

- Automatic flare detection
- Feature engineering
- Spectral feature extraction
- Solar flare forecasting
- Solar flare nowcasting
- Deep Learning models

---

## Installation

Clone the repository

```bash
git clone https://github.com/itz-ayushimishra/Aditya-L1-Solar-Flare-Forecasting.git
```

Move into the project directory

```bash
cd Aditya-L1-Solar-Flare-Forecasting
```

Install the required packages

```bash
pip install -r requirements.txt
```

Run the data extraction pipeline

```bash
python Scripts/main.py
```

Generate all light curve plots

```bash
python Scripts/plot_all_lightcurves.py
```

Generate the light curve summary

```bash
python Scripts/lightcurve_summary.py
```

---

## Contributors

- Ayushi Mishra
- Team Members (to be added)

---

## License

This project is intended for academic and research purposes.