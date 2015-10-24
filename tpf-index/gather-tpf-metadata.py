"""Grab the metadata from a set of TPF files and save it into a csv table.
"""
import os
import time
from urllib import request
from collections import OrderedDict

from astropy import log
from astropy.io import fits


log.setLevel("DEBUG")

# Configuration constants
INPUT_FN = "k2-c04-tpf-urls.txt"
OUTPUT_FN = "k2-c04-tpf-metadata.csv"
TMPDIR = "/tmp/"
MAX_ATTEMPTS = 50
SLEEP_BETWEEN_ATTEMPTS = 30
IGNORE_SHORT_CADENCE = False


class TPFFile(object):
    """Represent a Target Pixel File (TPF) as obtained from the MAST archive.

    Parameters
    ----------
    path : str
        Path or url to the tpf file.
    """
    def __init__(self, path):
        self.path = path.strip()
        attempt = 1
        while attempt <= MAX_ATTEMPTS:
            try:
                self.fits = fits.open(path, memmap=True)
                attempt = 99
            except Exception as e:
                if attempt == MAX_ATTEMPTS:
                    log.error("{}: max attempts reached".format(path))
                    raise e
                # Else try again after a sleep
                log.warning("{}: attempt {} failed: {}".format(path, attempt, e))
                log.warning("Now sleeping for {} sec".format(SLEEP_BETWEEN_ATTEMPTS))
                time.sleep(SLEEP_BETWEEN_ATTEMPTS)
                attempt += 1

    def header(self, kw, ext=0):
        """Returns the FITS header for the desired extension."""
        return self.fits[ext].header[kw]

    def get_metadata(self):
        """Returns a dictionary containing the metadata we care about."""
        meta = OrderedDict()
        for kw in ["OBJECT", "KEPLERID", "CHANNEL", "MODULE", "OUTPUT",
                   "CAMPAIGN", "OBSMODE", "RA_OBJ", "DEC_OBJ", "KEPMAG"]:
            meta[kw] = self.header(kw)
        for kw in ["LC_START", "LC_END", "GAIN", "READNOIS"]:
            meta[kw] = self.header(kw, ext=1)
        for kw in ["NAXIS1", "NAXIS2", "CRPIX1", "CRPIX2", "CRVAL1", "CRVAL2",
                   "CDELT1", "CDELT2", "PC1_1", "PC1_2", "PC2_1", "PC2_2",
                   "CRVAL1P", "CRVAL2P"]:
            meta[kw] = self.header(kw, ext=2)
        meta["cadenceno_begin"] = self.fits[1].data["CADENCENO"][0]
        meta["cadenceno_end"] = self.fits[1].data["CADENCENO"][-1]
        meta["path"] = self.path
        return meta

    def get_csv_header(self):
        """Returns the header line for the csv file."""
        meta = self.get_metadata()
        return ",".join([kw.lower() for kw in meta])

    def get_csv_row(self):
        """Returns the data line for the csv file."""
        meta = self.get_metadata()
        # Surely the values will never contain a comma right?
        return ",".join([str(meta[kw]) for kw in meta])


def download_file(url, local_filename, chunksize=16*1024):
    """Download a large file straight to disk."""
    with request.urlopen(url) as response, open(local_filename, 'wb') as f:
        while True:
            chunk = response.read(chunksize)
            if not chunk:
                break
            f.write(chunk)


if __name__ == "__main__":
    with open(OUTPUT_FN, "w") as out:
        with open(INPUT_FN, "r") as urls:
            for idx, url in enumerate(urls.readlines()):
                url = url.strip()
                # Ignore short cadence files?
                if IGNORE_SHORT_CADENCE and "spd-targ" in url:
                    continue
                # Try opening the file and adding a csv row
                try:
                    log.debug("Downloading {}".format(url))
                    tmp_fn = os.path.join(TMPDIR, os.path.basename(url))
                    download_file(url, tmp_fn)

                    log.debug("Reading {}".format(tmp_fn))
                    tpf = TPFFile(tmp_fn)
                    if idx == 0:
                        out.write(tpf.get_csv_header() + "\n")
                    out.write(tpf.get_csv_row() + "\n")
                    out.flush()
                except Exception as e:
                    log.error("{}: {}".format(url, e))
                finally:
                    # Ensure the temporary file is deleted
                    log.debug("Removing {}".format(tmp_fn))
                    try:
                        os.unlink(tmp_fn)
                    except Exception:
                        pass

    out.close()
