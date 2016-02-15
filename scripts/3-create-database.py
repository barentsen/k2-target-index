"""Creates an SQLite database detailing all the K2 target pixel files.

TODO
----
* Sort the final table by EPIC ID.
* Add an index to the sqlite table?
"""
import glob
import logging
import sqlite3

import pandas as pd


log = logging.getLogger(__name__)
log.setLevel("INFO")


CSV_FILENAME = "../k2-target-pixel-files.csv"
SQLITE_FILENAME = "../k2-target-pixel-files.db"


if __name__ == "__main__":
    log.info("Reading the data")
    df = pd.concat([pd.read_csv(fn)
                    for fn
                    in glob.glob("intermediate-data/*metadata.csv")])

    # Write to the CSV file
    log.info("Writing {}".format(CSV_FILENAME))
    df.to_csv(CSV_FILENAME, index=False)

    # Write the SQLite table
    log.info("Writing {}".format(SQLITE_FILENAME))
    con = sqlite3.connect(SQLITE_FILENAME)
    df.to_sql(name='tpf', con=con, if_exists='replace', index=False)
