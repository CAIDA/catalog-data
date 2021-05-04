~~~json
{
    "id": "how_to_annotate_a_traceroute_with_ixp",
    "name": "How to Annotate a Traceroute with IXP",
    "description": "The following solution will return a list of IXP names given IP addresses",
    "tags": [
      "ixps", 
      "internet exchange points", 
      "ip address",
      "ip"
    ],
    "links": ["dataset:ixps"],
    "authors":[
        {
            "person": "person:lee__nicole",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## Solution

Given a list of IP addresses, this following solution will return a list of correseponding IXP names.

load_traceroute() takes in one input:
- `path`: Path to jsonl file of IXPs, which can be found here: [ixps dataset](https://www.caida.org/catalog/datasets/ixps/) under ixs_*.jsonl files

and outputs:
- `ixpdb`: pyasn database
- `diction`: Dictionary to map to names of IXPs

annotate_traceroute() takes in three inputs:

- List of IP addresses
- `ixpdb`: pyasn database (from load_traceroute())
- `diction`: Dictionary to map to names of IXPs (from load_traceroute())
- `ips`: List of ip addresses

and prints:
- `final`: Array indicating corresponding IXP or invalid IP address note

**Usage:** `python3 ixp-annotations.py [path to jsonl file] [ip address] [ip address] ...`

i.e. `python3 ixp-annotations.py ixp.jsonl '198.32.231.77' '10'` will yield 
~~~
Invalid IP:  10
['npIX PTS', None]
~~~

~~~python

import json
import numpy as np
import pyasn
import os

def load_traceroute(path):
    """
    Parses provided IXP dataset and creates a pyasn compatible database and dictionary to be used in the next function.
    """
    temp_file = "_ixp.dat"
    with open(path) as f:
        next(f)
        data = []
        diction = {}
        i = 1
        # Gathers data from files and sets up format
        for line in f:
            obj = json.loads(line)
            name = obj['name']
            diction[i] = name
            recorded_ipv4 = list(map(lambda x: x+"\t%d"%i, obj['prefixes']['ipv4']))
            recorded_ipv6 = list(map(lambda x: x+"\t%d"%i, obj['prefixes']['ipv6']))
            data+=(recorded_ipv4+recorded_ipv6)
            i+=1
        # Writes data into file
        hdrtxt = '; IP-ASN32-DAT file\n; Original file : <Path to a rib file>\n; Converted on  : temp\n; CIDRs         : 512490\n;'
        np.savetxt(temp_file, data, header=hdrtxt,fmt='%s')
        ixpdb = pyasn.pyasn(temp_file)
        # Removes created file
        os.remove(temp_file)
        return ixpdb, diction
                
def annotate_traceroute(ixpdb, diction, ips):
    """
    Inputs a path to data file and a list of IP addresses and returns a corresponding list of IXP names.
    """
    # Converts all into IP address format, appends None if not IP address
    ixp_list = [None]*len(ips)
    for index in range(len(ips)):
        # Checks if address is valid
        try:
            ixpdb.lookup(ips[index])
        except ValueError:
            print("Invalid IP: ", ips[index])
            continue  
        # Looks up IP address in IXP database
        if ixpdb.lookup(ips[index])[1]:
            ixp_list[index] = diction[ixpdb.lookup(ips[index])[0]]
        else:
            continue                
    print(ixp_list)
~~~

## Background

### What is an Internet Exchange Point (IXP)?
- An IXP is a physical infrastructure that allow Internet Service Providers (ISPs), Content Delivery Networks(CDNs), and other organizations to exchange Internet traffic between their networks
- [IXPs are managed by one of the following](https://www.internetsociety.org/issues/ixps/): non-profit organizations, associations of ISPs, operator-neutral for-profit companies, university or government agencies, informal associations of networks

### What is an IP address?
- IP addresses are unique identifiers that connect devices to the Internet network for communication purposes

### What is a prefix?
- An IP address has two sections: host and network
- The network section makes up the first portion and the host section makes up the seond
- Thus, each network address (prefix) consists of a number of unique host addresses
- The goal of this solution is to determine which IXP a host IP addresses belongs to through checking whether a host IP is within range of provided prefixes

### Why use pyasn?
- pyasn allows for quick lookups to determine whether an IP address is within a prefix
- For the purpose of this solution, we've used pyasn to match to a number corresponding to an IXP name of an IP address

## Caveats
- Requires permission to write files
