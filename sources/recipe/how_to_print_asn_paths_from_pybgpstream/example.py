#!/usr/bin/env python3

#import the low level _pybgpsteam library and other necessary libraries
from pybgpstream import BGPStream
from ipaddress import ip_network
import time
import sys
import requests

# Initialize BGPStream, with routeviews-stream project, filtering for amsix.
stream = BGPStream(project="routeviews-stream", filter="router amsix")
# The stream will not load new data till its done with the current pulled data.
stream.set_live_mode()
print("starting stream...", file=sys.stderr)
for record in stream.records():
    rec_time = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(record.time))
    for elem in record:
        prefix = ip_network(elem.fields['prefix'])
        # Only print elements that are announcements (BGPElem.type = "A").
        if elem.type == "A":
            as_path = elem.fields['as-path'].split(" ")
            # Print all elements with 16509 in the path.
            if '16509' in as_path:
                print(f"peer asn: {elem.peer_asn} as path: {as_path} "
                      f"communities: {elem.fields['communities']} "
                      f"timestamp: {rec_time}")
