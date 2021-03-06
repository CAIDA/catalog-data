~~~json
{
    "id" : "how_to_print_records_from_pybgpstream",
    "name": "How to print records from pybgpstream",
    "description":"The recipe should show how to print elements from records of pybgpstream data.",

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

This solution should show how to print element records from a specific pybgpstream. The solution prints the first 100 records from a BGPStream from the routeviews-stream project, and filtering by the router, amsix.

## Solution

```python
#!/usr/bin/env python3

# Import pybgpsteam and other necessary libraries
from pybgpstream import BGPStream
import time

# Initialize BGPStream, with data from routeviews-stream for router amsix.
stream = BGPStream(project='routeviews-stream', filter="router amsix")

# Counter to stop BGPStream after X amount of prints.
counter = 0

# Print records yielded from stream.records() in a bgpreader-like format.
for record in stream.records():
    # Print the first 100 records found.
    if counter == 100:
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
```

### Usage

To run this script, you may need to install [pybgpstream](https://bgpstream.caida.org/download). Below is how to install with pip. For other ways click the link above. If there are any issue, look [here](https://bgpstream.caida.org/docs/install) for more help.

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
 - For more information on how to use pybgpstream, you can also visit our page [here](https://dev.catalog.caida.org/details/recipe/how_to_use_pybgpstream)

### Caveats
 - This script only prints the first 100 elements in the record of the specified BGPStream. 
   - Playing around with the inputs for ```stream``` will result in different output. Check out the pybgpstream documetentation to find how to adjust the BGPStream with other inputs.