"""Harvests a K2 Campaign's target pixel file metadata from MAST.
"""
import os
import sys
import time
from collections import OrderedDict
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from astropy import log
from astropy.io import fits


log.setLevel("DEBUG")

# Configuration constants
TMPDIR = "/tmp/"  # Must have enough space to store large short-cadence files
MAX_ATTEMPTS = 50  # How many times do we try to obtain & open a file?
SLEEP_BETWEEN_ATTEMPTS = 30  # seconds
IGNORE_SHORT_CADENCE = False


class TargetPixelFile(object):
    """Represent a Target Pixel File (TPF) as obtained from the MAST archive.

    Parameters
    ----------
    path : str
        Path or url to the tpf file.

    url : str, optional
        Public URL of the file, to be stored as metadata.
        (Defaults to the value of `path`.)
    """
    def __init__(self, path, url=None):
        self.path = path.strip()
        self.url = url
        if url is None:
            self.url = self.path
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
        """Returns the FITS header keyword for a specified extension.

        Returns the empty string if a keyword is Undefined or non-existant.
        """
        try:
            value = self.fits[ext].header[kw]
        except KeyError:  # Keyword does not exist
            return ""
        if isinstance(value, fits.Undefined):  # Keyword undefined
            return ""
        return value

    def get_metadata(self):
        """Returns a dictionary containing only the metadata we care about."""
        meta = OrderedDict()
        meta["filename"] = os.path.basename(self.url)
        meta["url"] = self.url
        filesize_mb = os.path.getsize(self.path) / 1048576.  # MB
        meta["filesize"] = "{:.1f}".format(filesize_mb)
        for kw in ["OBJECT", "KEPLERID", "OBSMODE", "CAMPAIGN",
                   "CHANNEL", "MODULE", "OUTPUT",
                   "RA_OBJ", "DEC_OBJ", "KEPMAG"]:
            meta[kw] = self.header(kw)
        meta["cadenceno_start"] = self.fits[1].data["CADENCENO"][0]
        meta["cadenceno_end"] = self.fits[1].data["CADENCENO"][-1]
        for kw in ["LC_START", "LC_END", "GAIN", "READNOIS", "MEANBLCK",
                   "CDPP3_0", "CDPP6_0", "CDPP12_0"]:
            meta[kw] = self.header(kw, ext=1)
        meta["npix"] = (self.fits[2].data > 0).sum()  # No of pixels downlinked
        for kw in ["NAXIS1", "NAXIS2", "CRPIX1", "CRPIX2", "CRVAL1", "CRVAL2",
                   "CDELT1", "CDELT2", "PC1_1", "PC1_2", "PC2_1", "PC2_2",
                   "CRVAL1P", "CRVAL2P"]:
            meta[kw] = self.header(kw, ext=2)
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
    response = urlopen(url)
    with open(local_filename, 'wb') as f:
        while True:
            chunk = response.read(chunksize)
            if not chunk:
                break
            f.write(chunk)


def write_metadata_table(input_fn, output_fn):
    """
    Parameters
    ----------
    input_fn : str
        Path to a text file listing the URLs of all the target pixel files
        to be analyzed.

    output_fn : str
        Path to the csv file that will be created.  If the file already exists,
        it will be overwritten.
    """
    # Main routine: download target pixel fiels & produce the metadata table
    with open(output_fn, "w") as out:
        with open(input_fn, "r") as urls:
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
                    tpf = TargetPixelFile(tmp_fn, url=url)
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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        log.error("Provide the campaign number as the first and only argument.")
        sys.exit(1)
    else:
        campaign = int(sys.argv[1])
        input_fn = "k2-c{:02d}-tpf-urls.txt".format(campaign)
        output_fn = "tmp/k2-c{:02d}-tpf-metadata.csv".format(campaign)
        write_metadata_table(input_fn, output_fn)
