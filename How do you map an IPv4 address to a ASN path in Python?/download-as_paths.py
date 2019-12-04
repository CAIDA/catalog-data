#!/usr/bin/env python

import pybgpstream
stream = pybgpstream.BGPStream(
    from_time="2017-07-07 00:00:00", until_time="2017-07-07 00:10:00 UTC",
    collectors=["route-views.sg", "route-views.eqix"],
    record_type="updates"
)

for elem in stream:
    # record fields can be accessed directly from elem
    asn_path = elem.fields["as-path"]
    prefix = elem.fields["prefix"]
    print(prefix+"\t"+asn_path)
