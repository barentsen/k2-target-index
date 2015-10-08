"""Save the footprints of all K2 campaigns as JSON files.

"""
import json
from collections import OrderedDict

import numpy as np

from astropy.table import Table
from astropy import log

from K2fov import fov
from K2fov.K2onSilicon import getRaDecRollFromFieldnum

from astropy.coordinates import SkyCoord

"""Configuration constants"""
# Which channels are no longer in use?
# Note: K2fov defines the FGS chips as "channels" 85-88
CHANNELS_TO_IGNORE = [5, 6, 7, 8, 17, 18, 19, 20,
                      85, 86, 87, 88]
CAMPAIGNS = Table.read("k2-campaigns.csv")


def get_metadata(campaign):
    """Returns (start_time, stop_time, comments) for each campaign

    Times are given as UTC dates and are approximate.
    """
    campaign_idx = CAMPAIGNS["campaign"] == campaign
    start = CAMPAIGNS[campaign_idx]["start"][0]
    stop = CAMPAIGNS[campaign_idx]["stop"][0]
    comments = CAMPAIGNS[campaign_idx]["comments"][0]
    return (start, stop, comments)


def get_footprint(campaign):
    ra, dec, scRoll = getRaDecRollFromFieldnum(campaign)
    # convert from SC roll to FOV coordinates
    # do not use the fovRoll coords anywhere else
    # they are internal to this script only
    fovRoll = fov.getFovAngleFromSpacecraftRoll(scRoll)
    kfov = fov.KeplerFov(ra, dec, fovRoll)
    return (ra, dec, scRoll, kfov.getCoordsOfChannelCorners())


if __name__ == "__main__":

    for campaign in range(14):
        # Obtain the metadata
        start, stop, comments = get_metadata(campaign)
        ra_bore, dec_bore, roll, corners = get_footprint(campaign)

        # Convert the footprint into a user-friendly format
        channels = OrderedDict([])
        for ch in np.arange(1, 89, dtype=int):
            if ch in CHANNELS_TO_IGNORE:
                continue  # certain channel are no longer used
            idx = np.where(corners[::, 2] == ch)
            mdl = int(corners[idx, 0][0][0])
            out = int(corners[idx, 1][0][0])
            channel_name = "{}".format(ch)
            ra = corners[idx, 3][0]
            dec = corners[idx, 4][0]
            crd = SkyCoord(ra, dec, unit='deg')
            glon = crd.galactic.l
            glat = crd.galactic.b
            #coords = [[ra[i], dec[i]] for i in [0, 1, 2, 3, 0]]
            #channels[channel_name] = coords
            channels[channel_name] = OrderedDict([
                                        ('module', str(mdl)),
                                        ('output', str(out)),
                                        ('corners_ra', list(ra)),
                                        ('corners_dec', list(dec)),
                                        ('corners_glon', list(glon.value)),
                                        ('corners_glat', list(glat.value)),
                                        ])

        # Add the metadata to the JSON dictionary
        output = OrderedDict([
                    ("campaign", campaign),
                    ("start", start),
                    ("stop", stop),
                    ("ra", ra_bore),
                    ("dec", dec_bore),
                    ("roll", roll),
                    ("comments", comments),
                    ("channels", channels)
                    ])

        # Finally, write the JSON file
        output_fn = "k2-c{:02d}-footprint.json".format(campaign)
        log.info("Writing {}".format(output_fn))
        json.dump(output, open(output_fn, "w"), indent=2)
