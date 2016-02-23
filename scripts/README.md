# Scripts

This directory contains the scripts that are used to create the index tables
of all Target Pixel Files (TPF).

## Usage

The index tables are created in three steps:

* `python 1-crawl-mast.py {CAMPAIGN}` creates a list of the URLs of all the target pixel files of the given Campaign number and writes the output to `intermediate-data/k2-c{CAMPAIGN}-tpf-urls.txt`.
* `python 2-analyze-target-pixel-files.py {CAMPAIGN}` extracts metadata for all the TPF files that were found in the first step, and writes the output to a CSV table called `intermediate-data/k2-c{CAMPAIGN}-tpf-metadata.csv`.
* `python 3-create-csv-db.py` collates all the metadata tables created in step 2 into a single user-friendly CSV table, called `k2-target-pixel-files.csv.gz` .
* `python 4-create-sqlite-db.py` create an SQLite table from the CSV table, with a limited number of columns to keep the file size small.
* `python 5-print-summary-stats.py` prints a few useful summary statistics of the dataset.
