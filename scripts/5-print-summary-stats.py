"""Produces a summary overview of the K2 data released so far."""
import sqlite3

KEPLER_PIXEL_SIZE = 3.98  # arcsec
KEPLER_PIXEL_AREA = (KEPLER_PIXEL_SIZE * KEPLER_PIXEL_SIZE) / (60**4)  # deg^2
CAMPAIGNS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 91, 92]

db_connection = sqlite3.connect("../k2-target-pixel-files.db")
cursor = db_connection.cursor()


def query(sql):
    cursor.execute(sql)
    return cursor.fetchone()


def print_summary(campaign='all', obsmode='long cadence'):
    sql = ("SELECT COUNT(*), SUM(npix), SUM(filesize)/1000 "
           "FROM tpf WHERE obsmode = '{}'".format(obsmode))
    if campaign != 'all':
        sql += ' AND campaign = {}'.format(campaign)
    res = query(sql)
    ntpf, npix, filesize_gb = res
    square_degrees = npix * KEPLER_PIXEL_AREA
    print("C{} {}: {} masks, {:.1f} Mpix, {:.1f} deg^2, {:.0f} GB".format(campaign, obsmode, ntpf, npix/1e6, square_degrees, filesize_gb))


if __name__ == "__main__":
    for obsmode in ["short cadence", "long cadence"]:
        for campaign in CAMPAIGNS:
            print_summary(campaign, obsmode)
        print_summary(campaign='all', obsmode=obsmode)
