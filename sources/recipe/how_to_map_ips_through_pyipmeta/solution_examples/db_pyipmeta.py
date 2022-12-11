#!/usr/bin/env python

import pyipmeta

ipm = pyipmeta.IpMeta(providers=["maxmind"], time="20191230")
filename = "ipnames.txt"
for line in open("ipnames.txt", "r"):
    sline = line.strip()
    print("Querying Maxmind for an IP address " + sline + ":")
    (res1,) =ipm.lookup(sline) 
    print(res1)
    #print(res2)
del ipm
