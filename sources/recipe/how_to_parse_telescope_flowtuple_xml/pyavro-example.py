# Example code that uses the AvroFlowtuple4Reader extension class to
# count flowtuples via a perFlowtuple callback method

import sys
from collections import defaultdict
from pyavro_stardust.flowtuple4 import AvroFlowtuple4Reader, \
        Flowtuple4AttributeNum, Flowtuple4AttributeStr, \
        Flowtuple4AttributeNumArray

counter = 0
protocols = defaultdict(int)

ttls = defaultdict(int)
flags = defaultdict(int)
sizes = defaultdict(int)

# Incredibly simple callback that simply increments a global counter for
# each flowtuple, as well as tracking the number of packets for each
# IP protocols
#
# We also report some stats on the most common TTLs, packet sizes and TCP flag
# combinations that our flowtuple records contain
def perFlowtupleCallback(ft, userarg):
    global counter, protocols
    counter += 1

    a = ft.asDict(True)
    proto = a["protocol"]
    pktcnt = a["packets"]

    protocols[proto] += pktcnt

    if "common_ttls" in a:
        for t in a["common_ttls"]:
            ttls[t['value']] += t['freq']

    if "common_pkt_sizes" in a:
        for s in a["common_pkt_sizes"]:
            sizes[s['value']] += s['freq']

    if "common_tcp_flags" in a:
        for f in a["common_tcp_flags"]:
            flags[f['value']] += f['freq']

def run():

    # sys.argv[1] must be a valid wandio path -- e.g. a swift URL or
    # a path to a file on disk
    ftreader = AvroFlowtuple4Reader(sys.argv[1])
    ftreader.start()

    # This will read all flowtuples and call `perFlowtupleCallback` on
    # each one
    ftreader.perAvroRecord(perFlowtupleCallback)

    ftreader.close()

    # Display our final result
    print("Total flowtuples:", counter)
    for k,v in protocols.items():
        print("Protocol", k, ":", v, "packets")

    print()
    for k,v in ttls.items():
        print("TTL", k, ":", v, "packets")

    print()
    for k,v in sizes.items():
        print("Packet Size", k, ":", v, "packets")

    print()
    for k,v in flags.items():
        print("TCP Flags", k, ":", v, "packets")

run()