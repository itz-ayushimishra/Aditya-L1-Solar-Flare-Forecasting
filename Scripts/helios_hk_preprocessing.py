from pathlib import Path
import zipfile

from astropy.io import fits
from astropy.table import Table

from config import *

PAYLOAD = "HEL1OS"

RAW_FOLDER = RAW_DATA / PAYLOAD
PROCESSED_FOLDER = PROCESSED_DATA / PAYLOAD


def create_output_folder(date):

    folder = PROCESSED_FOLDER / date

    folder.mkdir(parents=True, exist_ok=True)

    return folder


zip_files = list(RAW_FOLDER.glob("*.zip"))

for current_zip in zip_files:

    print("=" * 70)
    print(current_zip.name)
    print("=" * 70)

    parts = current_zip.stem.split("_")
    date = parts[1]

    with zipfile.ZipFile(current_zip, "r") as zip_ref:

        for file in zip_ref.namelist():

            if file.endswith("hk.fits"):

                print("Opening")
                print(file)

                with zip_ref.open(file) as fits_file:

                    hdul = fits.open(fits_file)

                    table = Table(hdul[1].data)

                    df = table.to_pandas()

                    output_folder = create_output_folder(date)

                    output_file = output_folder / "HouseKeeping.csv"

                    df.to_csv(output_file, index=False)

                    print("Saved ->", output_file)

                    hdul.close()

print("\nFinished.")