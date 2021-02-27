~~~json
{
    "id" : "how_to_print_rpki_data_from_pybgpstream",
    "name": "How to print rpki data from pybgpstream",
    "description":"This solution should show the user how to get RPKI data from interfaces taken from a pybgpstream.",
    "links": [
        {
            "to": "software:bgpstream"
        }
    ],
    "tags": [
        "asn",
        "rpki",
        "routeviews"
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

This recipe should show the user how to use pybgpstream to print RPKI data using routeviews. The solution prints json data to STDOUT with data taken from routeviews API given input ip addresses from pybgpstream. 

## Solution

The output from the routeviews API is a json of the interface (ip address), and its parent asn, data on its stability and timestamp.

For example, an interafce pulled from pybgpstream may be `2001:7fb:fe0c::/48`. This interface is then placed in the link to the API in the code below. This link produces a json output which is then printed to STDOUT. For this example, you may get a similar output to this:

```text
{
    '2001:7fb:fe0c::/48': {
        'asn': [
            {'12654': 'valid'}
        ], 
        'timestamp': '2020-09-24 16:00:01'
    }
}
```

The data can also be seen on the API itself by follwing this [link](https://api.routeviews.org/rpki?prefix=2001:7fb:fe0c::/48).

```python
#!/usr/bin/env python3

from pybgpstream import BGPStream
from ipaddress import ip_network
import requests
import sys

# Initialize BGPStream, with routeviews-stream project, filtering for amsix.
stream = BGPStream(project="routeviews-stream", filter="router amsix")
print("starting stream...", file=sys.stderr)
for record in stream.records():
    for elem in record:
        prefix = ip_network(elem.fields['prefix'])
        if elem.type == "A":
            # Lookup RPKI state based on announced route.
            request = requests.get(f"https://api.routeviews.org/rpki?prefix={prefix}")
            print(request.json())
```

### Usage

To run this script, you may need to install [pybgpstream](https://bgpstream.caida.org/download). Below is how to install with pip. For other ways click the link above.

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

What is RPKI?
 - RPKI is a security framework that helps network operators make more informed and secure routing decisions.
 - RPKI is a way to define data in an out-of-band system such that the information that are exchanged by BGP can be validated to be correct. 
 - For more information on RPKI, you can read more about it [here](https://rpki.readthedocs.io/en/latest/about/faq.html).

### Caveats
- The script above uses specific inputs when initializing the BGPStream object meaning their is more data that can be taken by adjusting these inputs. Playing around with the inputs for ```stream``` will result in different outputs. Check out the pybgpstream documetentation to find ways to adjust the BGPStream with other inputs.