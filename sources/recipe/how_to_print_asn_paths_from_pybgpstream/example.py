#!/usr/bin/env python3

#import the low level _pybgpsteam library and other necessary libraries
from pybgpstream import BGPStream
from ipaddress import ip_network
import time
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("target", nargs="*", type=str, help="ASNs we are looking up")
parser.add_argument("-d", "--debug", type=int, help="Number of traces")
args = parser.parse_args()

# Initialize BGPStream with RIPE RIS LIVE and collector rrc00
stream = BGPStream(project="ris-live",
                   collectors=["rrc00"],
                   filter="collector rrc00")

# The stream will not load new data till it's done with the current pulled data.
stream.set_live_mode()
print("starting stream...", file=sys.stderr)

# Counter
counter = 0

for record in stream.records():
    # Handles debug option
    if args.debug is None:
        pass
    elif counter >= args.debug:
        break
    else:
        counter += 1

    rec_time = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(record.time))
    for elem in record:
        try:
            prefix = ip_network(elem.fields['prefix'])
            # Only print elements that are announcements (BGPElem.type = "A").
            if elem.type == "A" or elem.type == "R":
                as_path = elem.fields['as-path'].split(" ")
                # Print all elements with specified in args.target
                for target in args.target:
                    if target in as_path:
                        print(f"Peer asn: {elem.peer_asn} AS Path: {as_path} "
                                f"Communities: {elem.fields['communities']} "
                                f"Timestamp: {rec_time}")

        # Reports and skips all KeyError
        except KeyError as e:
            print("KEY ERROR, element ignored: KEY=" + str(e), file=sys.stderr)
            continue

