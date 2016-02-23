# K2 Target Index

***A user-friendly list of all the K2 target pixel files and their properties.***

This repository provides a list of the filenames, urls, and useful metadata 
of all the K2 Target Pixel Files (TPF) that are available
in the [data archive at MAST](https://archive.stsci.edu/pub/k2/target_pixel_files/).


## Contents

* `k2-target-pixel-files.csv.gz`: a table of all target pixel files in gzipped CSV format. 
* `k2-target-pixel-files.db`: a subset of the columns in the CSV table in SQLite format.


## Columns

The vast majority of the columns correspond directly to header keywords
in the target pixel files.  Hence more information about their meaning
can be found in the Kepler Instrument and Data Characteristics Handbooks.

Note that the SQLite file only contains a subset of these columns to keep its size small.

* `filename`: target pixel filename.
* `url`: full HTTP URL of the target pixel file.
* `filesize`: size of the target pixel file (MB). 
* `object`: name of the target, i.e. `EPIC XXXXXXXXXX`.
* `keplerid`: EPIC ID number.
* `obsmode`: one of `long cadence` or `short cadence`.
* `campaign`: K2 Campaign number, e.g. `1` or `2`.
* `data_rel`: K2 data release number.
* `channel`: focal plane channel number.
* `module`: focal plane module number.
* `output`: focal plane module output number.
* `ra_obj`: J2000 Right Ascension of the target in the EPIC catalog (decimal degrees).  This position is not corrected for proper motion and may hence fall outside the aperture mask.
* `dec_obj`: Declination of the target in the EPIC catalog (decimal degrees).
* `kepmag`: Kepler magnitude of the target in the EPIC catalog.
* `cadences`: total number of cadences recorded in the file.
* `lc_start`: time of the first cadence.
* `lc_stop`: time of the last cadence.
* `gain`: detector gain.
* `readnoise`: detector read noise.
* `meanblck`: back ground estimate.
* `cddp3_0`: 3-hour CDPP estimate.
* `cddp6_0`: 6-hour CDPP estimate.
* `cddp12_0`: 12-hour CDPP estimate.
* `npix`: total number of pixels in the aperture mask.
* `naxis1`: size of the aperture mask in one direction.
* `naxis2`: size of the aperture mask in the other direction.
* `crpix1`, `crpix2`, `crval1`, `crval2`, `cdelt1`, `cdelt2`, `pc1_1`, `pc1_2`, `pc2_1`, `pc2_2`, `crval1p`, `crval2p`: WCS keywords.
* `corners`: ra,dec;ra,dec;ra,dec;ra,dec of the mask corners in decimal degrees.
* `ra_min`, `ra_max`, `dec_min`, `dec_max`: bounding box of the target mask in decimal degrees.


## Authors

Created by Geert Barentsen at the Kepler/K2 Guest Observer Office.
Please get in touch to report feedback or useful applications.
