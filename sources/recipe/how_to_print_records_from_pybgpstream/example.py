#!/usr/bin/env python3

# Import pybgpstream and other necessary libraries
from pybgpstream import BGPStream
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("print_amount", nargs=1, type=int, help="Number of prints")
args = parser.parse_args()

# Initialize BGPStream, with data from routeviews-stream for router amsix.
stream = BGPStream(project='routeviews-stream', filter="router amsix")

# Counter to stop BGPStream after X amount of prints.
counter = 0

# Print records yielded from stream.records() in a bgpreader-like format.
for record in stream.records():
    # Print the first X records found.
    if counter >= args.print_amount[0]:
        break
    else:
        counter += 1

    print(record.project, record.collector, record.router)
    # Make the date is human readable
    rec_time = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(record.time))
    for elem in record:
        # Print the current element in the record. Both are equivelent.
        # print(elem)
        print("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(
            elem.record_type,
            elem.type,
            rec_time,
            elem.project,
            elem.collector,
            elem.router,
            elem.router_ip,
            elem.peer_asn,
            elem.peer_address,
            elem._maybe_field("prefix"),
            elem._maybe_field("next-hop"),
            elem._maybe_field("as-path"),
            " ".join(elem.fields["communities"]) if "communities" in elem.fields else None,
            elem._maybe_field("old-state"),
            elem._maybe_field("new-state")
        ))
