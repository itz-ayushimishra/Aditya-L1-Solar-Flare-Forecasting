from pathlib import Path
import zipfile

from astropy.io import fits
from astropy.table import Table
import pandas as pd

from config import *

PAYLOAD = "HEL1OS"

RAW_FOLDER = RAW_DATA / PAYLOAD
PROCESSED_FOLDER = PROCESSED_DATA / PAYLOAD

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

def create_output_folder(date, detector):

    folder = PROCESSED_FOLDER / date / detector

    folder.mkdir(parents=True, exist_ok=True)

    return folder

def extract_lightcurve(zip_ref, filename, current_zip):

    print("\nOpening")
    print(filename)

    with zip_ref.open(filename) as fits_file:

        hdul = fits.open(fits_file)

        parts = current_zip.stem.split("_")
        date, time = parts[1], parts[2]

        for hdu in hdul[1:]:

            table = Table(hdu.data)
            df = table.to_pandas()

            detector = hdu.header["DETNAM"]
            elow = hdu.header["ELOW"]
            ehigh = hdu.header["EHIGH"]

            output_folder = create_output_folder(date, detector)

            output_file = output_folder / (
                f"LightCurve_{time}_{elow}_{ehigh}keV.csv"
            )

            df.to_csv(output_file, index=False)

            print(f"Saved -> {output_file}")

        hdul.close()

def extract_spectrum(zip_ref, filename, current_zip):

    print("\nOpening")
    print(filename)

    with zip_ref.open(filename) as fits_file:

        hdul = fits.open(fits_file)

        parts = current_zip.stem.split("_")
        date, time = parts[1], parts[2]

        table = Table(hdul[1].data)
        df = table.to_pandas()

        detector = hdul[1].header["DETNAM"]

        output_folder = create_output_folder(date, detector)

        output_file = output_folder / f"{detector}_Spectrum.csv"

        df.to_csv(output_file, index=False)

        print(f"Saved -> {output_file}")

        hdul.close()        

zip_files = list(RAW_FOLDER.glob("*.zip"))

for current_zip in zip_files:

    print("=" * 70)
    print(current_zip.name)
    print("=" * 70)

    with zipfile.ZipFile(current_zip, "r") as zip_ref:

        for file in zip_ref.namelist():

            if "lightcurve" in file.lower():

                extract_lightcurve(zip_ref, file, current_zip)

            elif "spectra" in file.lower():

                extract_spectrum(zip_ref, file, current_zip)