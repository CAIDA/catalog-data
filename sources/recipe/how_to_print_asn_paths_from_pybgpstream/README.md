~~~json
{
    "id" : "how_to_print_asn_paths_from_pybgpstream",
    "name": "How to print asn paths from pybgpstream",
    "description":"The recipe should show how to print specifc asn paths using data from pybgpstream.",

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

This solution should show the user how to print specific asn paths taken from records and elements of a pybgpstream. The solution prints the path from the BGPStream after specifying the routeviews-stream project, and filtering by the router, amsix. This recipe can take some time to fully run, for testing you may wish to interupt the program after a few minutes to check if the output is what you're hoping for.

## Solution

```python
#!/usr/bin/env python3

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
            # Print all elements with the asn 3356 in the path.
            if '3356' in as_path:
                print(f"Peer asn: {elem.peer_asn} AS Path: {as_path} "
                      f"Communities: {elem.fields['communities']} "
                      f"Timestamp: {rec_time}")
```

### Usage

To run this script, you may need to install [pybgpstream](https://bgpstream.caida.org/download). Below is how to install with pip. For other ways to install, click the link above.

```bash
pip3 install pybgpstream
```

To run this script, you may want to send the printed data from STDOUT to a file to reduce clutter.

```bash
./example.py > output.txt
```

## Background

What is pybgpstream?
 - pybgpstream is a Python open-source software framework for live and historical BGP data analysis, supporting scientific research, operational monitoring, and post-event analysis.
 - For more information on how to use pybgpstream, you can find their documentation [here](https://bgpstream.caida.org/docs)
 - For more information on how else to use pybgpstream, you can also visit our page [here](https://dev.catalog.caida.org/details/recipe/how_to_use_pybgpstream)

What does it mean to check the elem.type in the solution code?
 - The element type is part of the BGPElem class which can be found [here](https://bgpstream.caida.org/docs/api/pybgpstream/_pybgpstream.html#bgpelem).
   - "The type of the element, can be one of ‘R’ (ribs), ‘A’ (announcement), ‘W’ (withdrawal), ‘S’ (peer state), ‘’. (basestring, readonly)" - Documentation
   - Since we are looking for 

### Caveats
- The script above uses specific inputs when initializing the BGPStream object meaning their is more data that can be taken by adjusting these inputs. Playing around with the inputs for `stream` will result in different outputs. Check out the pybgpstream documetentation to find ways to adjust the BGPStream with other inputs.
- This script will run through all bgpstream records until it is complete. This will take a long time, it is recommend the user manually interrupts the script after a couple minutes if they don't intend to use all the data that will be printed.