#!/usr/bin/env python3

from pybgpstream import BGPStream
from ipaddress import ip_network
import requests
import sys
import json
import argparse

# Initialize BGPStream, with routeviews-stream project, filtering for amsix.
stream = BGPStream(project="routeviews-stream", filter="router amsix")
print("starting stream...", file=sys.stderr)

# Debug Option to limit number of traces
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", type=int, help="Number of traces")
args = parser.parse_args()

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

    for elem in record:
        prefix = ip_network(elem.fields['prefix'])
        if elem.type == "A":
            # Lookup RPKI state based on announced route.
            request = requests.get(f"https://api.routeviews.org/rpki?prefix={prefix}", verify=False)
            response = request.json()
            # Skip all None responses
            if response[str(prefix)] is not None:
                data = {
                    "prefix": str(prefix),
                    "rpki": response[str(prefix)],
                    "timestamp": response[str(prefix)]['timestamp']
                }
                # Output json to stdout
                print(json.dumps(data))
