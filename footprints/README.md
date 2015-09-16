# K2 Campaign footprints

The `json` files in this directory detail the field of view
of each active channel in each K2 campaign.

### Usage

The json file  for each campaign may be read into a Python dictionary
as follows:
```
import json
c4_footprint = json.load(open("k2-c04-footprint.json"))
```

The dictionary may then be used, e.g. plotting the footprint of channel 4:
```
import matplotlib.pyplot as pl
pl.figure()
pl.plot(c4_footprint['channels']['4']['corners_ra'],
        c4_footprint['channels']['4']['corners_dec'])
pl.show()
```

(Warning, the sky is a sphere, hence straight lines shown on this simple
plot will not *exactly* correspond to great circles on the sky.)
