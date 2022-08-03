~~~json
{
    "id" : "how_to_print_asn_paths_from_pybgpstream",
    "name": "How to print asn paths from pybgpstream",
    "description":"The recipe should show how to print specific asn paths using data from pybgpstream.",

    "links": [
        {
            "to": "software:bgpstream"
        }
    ],
    "tags": [
        "asn"
    ],
    "authors":[
        {
            "person": "person:wolfson__donald",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## Introduction

This solution should show the user how to print specific asn paths taken from records and elements of a pybgpstream. The solution prints the path from the BGPStream after specifying the RIS-LIVE project, and filtering by the collector rrc00 to enhance performance. This recipe can take some time to fully run, for testing you may wish to interupt the program after a few minutes to check if the output is what you're hoping for.

## Solution

~~~python
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
~~~

### Usage

To run this script, you may need to install [pybgpstream](https://bgpstream.caida.org/download). Below is how to install with pip. For other ways to install, click the link above. If there are any issue, look [here](https://bgpstream.caida.org/docs/install) for more help.

~~~bash
pip3 install pybgpstream
~~~

To run this script, you may want to send the printed data from STDOUT to a file to reduce clutter.

The debug option `-d` allows users to limit number of traces the program goes through to N to shorten execution time.

~~~bash
./example.py [-d N] ASN#1 ASN#2 ... ASN#N > output.txt
~~~

## Background

What is pybgpstream?
 - pybgpstream is a Python open-source software framework for live and historical BGP data analysis, supporting scientific research, operational monitoring, and post-event analysis.
 - For more information on how to use pybgpstream, you can find their documentation [here](https://bgpstream.caida.org/docs)
 - For more information on how else to use pybgpstream, you can also visit our page [here](https://dev.catalog.caida.org/details/recipe/how_to_use_pybgpstream)

What does it mean to check the elem.type in the solution code?
 - The element type is part of the BGPElem class which can be found [here](https://bgpstream.caida.org/docs/api/pybgpstream/_pybgpstream.html#bgpelem).
   - "The type of the element, can be one of ‘R’ (ribs), ‘A’ (announcement), ‘W’ (withdrawal), ‘S’ (peer state). (basestring, readonly)
   - We look for rib and announcement type element because they include data regarding AS path.

### Caveats
- The script above uses specific inputs when initializing the BGPStream object meaning their is more data that can be taken by adjusting these inputs. Playing around with the inputs for `stream` will result in different outputs. Check out the pybgpstream documetentation to find ways to adjust the BGPStream with other inputs.
- This script will run through all bgpstream records until it is complete. This will take a long time. It is recommended that the user to use the `-d` flag if they don't want all the data.