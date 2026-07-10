from pathlib import Path
import zipfile
from astropy.io import fits

PROJECT_ROOT = Path(__file__).resolve().parent.parent

zip_file = next((PROJECT_ROOT / "Raw_Data" / "HEL1OS").glob("*.zip"))

with zipfile.ZipFile(zip_file, "r") as zip_ref:

    target = None

    for file in zip_ref.namelist():

        if "lightcurve_cdte1.fits" in file:
            target = file
            break

    print("Opening:")
    print(target)

    with zip_ref.open(target) as fits_file:

        hdul = fits.open(fits_file)

        print("\n========== HDU INFO ==========")
        hdul.info()

        print("\n========== PRIMARY HEADER ==========")

        print(hdul[0].header)

        print("\n========== EXTENSION HEADER ==========")

        print(hdul[1].header)

        print("\n========== DATA ==========")

        print(hdul[1].data[:5])