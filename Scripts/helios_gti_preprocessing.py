from pathlib import Path
import zipfile

from astropy.io import fits
from astropy.table import Table

from config import *

PAYLOAD = "HEL1OS"

RAW_FOLDER = RAW_DATA / PAYLOAD
PROCESSED_FOLDER = PROCESSED_DATA / PAYLOAD

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)


def create_output_folder(date, detector):

    folder = PROCESSED_FOLDER / date / detector

    folder.mkdir(parents=True, exist_ok=True)

    return folder


def extract_gti(zip_ref, filename, current_zip):

    print("\nOpening")
    print(filename)

    with zip_ref.open(filename) as fits_file:

        hdul = fits.open(fits_file)

        parts = current_zip.stem.split("_")
        date = parts[1]

        table = Table(hdul[1].data)
        df = table.to_pandas()

        detector = (
            hdul[1]
            .header["EXTNAME"]
            .replace("GTI_", "")
            .upper()
        )

        output_folder = create_output_folder(date, detector)

        output_file = output_folder / "GTI.csv"

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

            if "gti" in file.lower() and file.endswith(".fits"):

                extract_gti(zip_ref, file, current_zip)

print("\nFinished extracting HEL1OS GTIs.")