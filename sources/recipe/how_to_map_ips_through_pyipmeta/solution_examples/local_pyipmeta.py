#!/usr/bin/env python

import _pyipmeta
import json

ipm = _pyipmeta.IpMeta()

# try getting a provider that exists
prov = ipm.get_provider_by_id(1)

# enables provider with local dataset
ipm.enable_provider(prov, "-b ./maxmind/2017-03-16.GeoLiteCity-Blocks.csv.gz -l ./maxmind/2017-03-16.GeoLiteCity-Location.csv.gz")

# runs geolocation on IPs specified in file
for line in open("ipnames.txt", "r"):
    sline = line.strip()
    print("Querying Maxmind for an IP address " + sline + ":")
    (res,) = ipm.lookup(sline)
    print(res)

