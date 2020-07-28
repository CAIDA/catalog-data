~~~
{
    "id": "how_to_annotate_a_traceroute_with_ixp",
    "name": "How to Annotate a Traceroute with IXP",
    "description": "The following solution will return a list of IXP names given IPv4 addresses",
    tags:[
      "ixps", 
      "internet exchange points", 
      "ip address",
      "ip"
    ]
}
~~~

## Solution

Given a list of IP addresses, this following function will return a list of correseponding IXP names. It takes in the following arguments:
- Path to jsonl file of IXPs, which can be found here: [ixps dataset](http://data.caida.org/datasets/ixps/) under ixs_*.jsonl files
- List of IP addresses

**Usage:** `python3 ixp-annotations.py [path to jsonl file] [ip address] [ip address] ...`

i.e. `python3 ixp-annotations.py ixp.jsonl '198.32.231.77' '10'` will yield `['npIX PTS', None]`

~~~python

import json
import ipaddress

def annotate_traceroute(path, ips):
    # Converts all into IP address format, appends None if not IP address
    ips_format = []
    for ip in ips:
        try:
            ips_format.append(ipaddress.ip_address(ip))
        except: 
            ips_format.append(None)
    ips_set = set(ips_format)
    final_set = [None]*len(ips)

    # Searches for IP address in json file
    with open(path) as f:
        next(f)
        for line in f:
            obj = json.loads(line)
            name = obj['name']
            for ip in obj['prefixes']['ipv4']:
                hosts = set(ipaddress.ip_network(ip).hosts())
                inside = hosts.intersection(ips_set)
                if len(inside) != 0:
                    for i, e in enumerate(ips_format):
                        if e in inside:
                            final_set[i] = name
    print(final_set)
~~~

## Background

### What is an Internet Exchange Point (IXP)?
- An IXP is a physical infrastructure that allow Internet Service Providers (ISPs), Content Delivery Networks(CDNs), and other organizations to exchange Internet traffic between their networks
- [IXPs are managed by one of the following](https://www.internetsociety.org/issues/ixps/): non-profit organizations, associations of ISPs, operator-neutral for-profit companies, university or government agencies, informal associations of networks

### Caveats
- This solution is only compatible with IPv4 addresses; IPv6 addresses will yield "None"
