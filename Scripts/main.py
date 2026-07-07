from pathlib import Path
import zipfile
import gzip
from astropy.io import fits
from astropy.table import Table
import pandas as pd

def extract_lightcurve(zip_ref, filename):

    print("\nOpening Light Curve...")
    print(filename)
    date = filename.split("/")[0].split("_")[3]
    detector = filename.split("/")[1]
    print("Date:", date)

    date_folder = Path("Processed_Data") / date
    date_folder.mkdir(exist_ok=True)

    with zip_ref.open(filename) as gz_file:

        with gzip.open(gz_file) as fits_file:

            hdul = fits.open(fits_file)

            table = Table(hdul[1].data)

            df = table.to_pandas()

            print(df.head())

            output_file = date_folder / f"{detector}_LightCurve.csv"

            df.to_csv(output_file, index=False)

            print("\nLight Curve saved successfully!")

def extract_gti(zip_ref, filename):

    print("\nOpening GTI...")
    print(filename)

    # Extract the date
    date = filename.split("/")[0].split("_")[3]
    print("Date:", date)

    # Extract the detector (SDD1 or SDD2)
    detector = filename.split("/")[-1].split("_")[3]
    print("Detector:", detector)

    date_folder = Path("Processed_Data") / date
    date_folder.mkdir(exist_ok=True)

    with zip_ref.open(filename) as gz_file:

        with gzip.open(gz_file) as fits_file:

            hdul = fits.open(fits_file)

            table = Table(hdul[1].data)

            df = table.to_pandas()

            if df.empty:
                print(f"GTI is empty ({detector}).")
            else:
                print(df.head())

            output_file = date_folder / f"{detector}_GTI.csv"
            df.to_csv(output_file, index=False)

            print("\nGTI saved successfully!")

def extract_spectrum(zip_ref, filename):

    print("\nOpening Spectrum...")
    print(filename)

    # Extract date
    date = filename.split("/")[0].split("_")[3]
    detector = filename.split("/")[1]

    date_folder = Path("Processed_Data") / date
    date_folder.mkdir(exist_ok=True)

    with zip_ref.open(filename) as gz_file:

        with gzip.open(gz_file) as fits_file:

            hdul = fits.open(fits_file)

            print("\n========== FITS FILE STRUCTURE ==========")
            hdul.info()

            print("\n========== PRIMARY HEADER ==========")

            for key, value in hdul[0].header.items():
                print(f"{key:12} : {value}")

            table = Table(hdul[1].data)

            # Convert FITS table to pandas
            df = table.to_pandas()

            # Save the original spectrum
            raw_output = date_folder / f"{detector}_Spectrum.csv"
            df.to_csv(raw_output, index=False)

            print("\nRaw Spectrum saved successfully!")

            # Test only first 10 spectra
            # df = df.head(10)

            # expanded_rows = []

            # # Go through every spectrum
            # for _, row in df.iterrows():

            #     channels = row["CHANNEL"]
            #     counts = row["COUNTS"]

            #     # Go through all 340 channels
            #     for channel, count in zip(channels, counts):

            #         expanded_rows.append({
            #             "SPEC_NUM": row["SPEC_NUM"],
            #             "TSTART": row["TSTART"],
            #             "TELAPSE": row["TELAPSE"],
            #             "EXPOSURE": row["EXPOSURE"],
            #             "CHANNEL": channel,
            #             "COUNTS": count
            #         })

            # # Create new dataframe
            # expanded_df = pd.DataFrame(expanded_rows)

            # # Show one complete spectrum
            # #spec2 = expanded_df[expanded_df["SPEC_NUM"] == 2]
            # # print("\nSpectrum 2 summary")
            # # print(spec2.head(20))
            # # print(spec2.tail(20))

            # # print("\nMaximum counts in Spectrum 2:")
            # # print(spec2["COUNTS"].max())
            # # print("\nChannel having maximum counts:")
            # # max_row = spec2.loc[spec2["COUNTS"].idxmax()]
            # # print(max_row)
            # # print("\nFirst non-zero channels:")
            # # print(spec2[spec2["COUNTS"] > 0].head(20))

            # # print("\nChecking which spectra contain signal...")

            # # signal = expanded_df.groupby("SPEC_NUM")["COUNTS"].sum()

            # # print(signal[signal > 0].head(20))

            # # print("\nFirst 20 rows:")
            # # print(expanded_df.head(20))

            # # print("\nFirst 10 rows of Spectrum 2:")
            # # print(expanded_df[expanded_df["SPEC_NUM"] == 2].head(10))

            # output_file = date_folder / f"{detector}_ExpandedSpectrum.csv"

            # expanded_df.to_csv(output_file, index=False)

            # print("\nExpanded Spectrum saved successfully!")


# Folder containing ZIP files
raw_data_folder = Path("Raw_Data")
processed_data_folder = Path("Processed_Data")
processed_data_folder.mkdir(exist_ok=True)

# Get all ZIP files
zip_files = list(raw_data_folder.glob("*.zip"))

print("ZIP files found:")

for file in zip_files:
    print(file.name)

for current_zip in zip_files:

    print("\n" + "=" * 50)
    print("Opening:", current_zip.name)
    print("=" * 50)

    with zipfile.ZipFile(current_zip, "r") as zip_ref:
        print("\n========== FILES INSIDE ZIP ==========\n")

        for file in zip_ref.namelist():
            print(file)

        print("\nSearching for data files...\n")

        for file in zip_ref.namelist():

            if file.endswith(".lc.gz"):
                print("Light Curve :", file)
                extract_lightcurve(zip_ref, file)

            elif file.endswith(".pi.gz"):
                print("Spectrum    :", file)
                extract_spectrum(zip_ref, file)

            elif file.endswith(".gti.gz"):
                print("GTI         :", file)
                extract_gti(zip_ref, file)