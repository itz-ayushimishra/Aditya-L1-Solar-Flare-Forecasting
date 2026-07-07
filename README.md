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

## Dataset

The dataset is hosted on Google Drive because it is too large to store on GitHub.

### Download

https://drive.google.com/drive/folders/1pWUoWb_oGE1jtIZCPxaoG2efrLtM96pR?usp=sharing

Download the following folders:

- Raw_Data
- Processed_Data

Place them in the project root directory so that the folder structure becomes:

Aditya_L1_Project/
│
├── Raw_Data/
├── Processed_Data/
├── Scripts/
├── requirements.txt
└── README.md

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

Move into the project

```bash
cd Aditya-L1-Solar-Flare-Forecasting
```

Install dependencies

```bash
pip install -r requirements.txt
```

Download the dataset from the Google Drive link above and place the folders inside the project directory.

Run the extraction pipeline (if required)

```bash
python Scripts/main.py
```

Generate light curve plots

```bash
python Scripts/plot_all_lightcurves.py
```
---

## Contributors

- Ayushi Mishra
- Team Members (to be added)

---

## License

This project is intended for academic and research purposes.