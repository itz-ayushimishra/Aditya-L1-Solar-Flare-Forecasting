from pathlib import Path
import zipfile

from astropy.io import fits
from astropy.table import Table

from config import *

PAYLOAD = "HEL1OS"

RAW_FOLDER = RAW_DATA / PAYLOAD
PROCESSED_FOLDER = PROCESSED_DATA / PAYLOAD

def create_output_folder(date, detector):

    folder = PROCESSED_FOLDER / date / detector

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

            if file.endswith("evt.fits"):

                print("Opening")
                print(file)

                with zip_ref.open(file) as fits_file:

                    hdul = fits.open(fits_file)

                    for hdu in hdul[1:]:

                        detector = hdu.header["DETNAM"]

                        table = Table(hdu.data)

                        df = table.to_pandas()

                        output_folder = create_output_folder(
                            date,
                            detector
                        )

                        output_file = (
                            output_folder /
                            f"{detector}_Events.csv"
                        )

                        df.to_csv(
                            output_file,
                            index=False
                        )

                        print("Saved ->", output_file)

                    hdul.close()

print("\nFinished.")