"""Export a CSV and SQLite database detailing all the K2 target pixel files.
"""
import glob
import logging
import sqlite3

import pandas as pd

from astropy import wcs

log = logging.getLogger(__name__)
log.setLevel("INFO")

# Output filenames
CSV_FILENAME = "../k2-target-pixel-files.csv.gz"
SQLITE_FILENAME = "../k2-target-pixel-files.db"


if __name__ == "__main__":
    log.info("Reading the data")
    df = pd.concat([pd.read_csv(fn)
                    for fn
                    in glob.glob("intermediate-data/*metadata.csv")])
    df = df.sort_values("keplerid")
    """
    for idx, row in df.iterrows():
        x, y = row['naxis1'], row['naxis2']
        # Corners (ra, dec) of the stamp
        metadata = {}
        metadata['CTYPE1'] = 'RA---TAN'
        metadata['CTYPE2'] = 'DEC--TAN'
        for kw in ['naxis1', 'naxis2', 'crpix1', 'crpix2', 'crval1', 'crval2',
                   'cdelt1', 'cdelt2', 'pc1_1', 'pc1_2', 'pc2_1', 'pc2_2',
                   'crval1p', 'crval2p']:
            metadata[kw] = row[kw]
        mywcs = wcs.WCS(metadata)
        corners = mywcs.all_pix2world([-0.5, -0.5, x-0.5, x-0.5],
                                      [-0.5, y-0.5, y-0.5, -0.5],
                                      0)
        # Bounding box in equatorial coordinates
        ra_min, ra_max = corners[0].min(), corners[0].max()
        dec_min, dec_max = corners[1].min(), corners[1].max()

    """
    # Write to the CSV file
    log.info("Writing {}".format(CSV_FILENAME))
    df.to_csv(CSV_FILENAME, index=False, compression="gzip")

    # Write the SQLite table
    log.info("Writing {}".format(SQLITE_FILENAME))
    con = sqlite3.connect(SQLITE_FILENAME)
    df.to_sql(name='tpf', con=con, if_exists='replace', index=False)
