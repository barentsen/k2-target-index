import sqlite3
import pandas as pd

CSV_FILENAME = "../k2-target-pixel-files.csv.gz"
SQLITE_FILENAME = "../k2-target-pixel-files.db"  # output

# Only export a subset of columns to keep the sqlite file compact
SQL_COLUMNS = ["filename", "url", "filesize", "keplerid", "obsmode",
               "campaign", "channel", "kepmag", "npix", "naxis1", "naxis2",
               "ra_min", "ra_max", "dec_min", "dec_max"]

if __name__ == "__main__":
    df = pd.read_csv(CSV_FILENAME)
    print("Writing {}".format(SQLITE_FILENAME))
    con = sqlite3.connect(SQLITE_FILENAME)
    df[SQL_COLUMNS].to_sql(name='tpf', con=con, if_exists='replace', index=False)
