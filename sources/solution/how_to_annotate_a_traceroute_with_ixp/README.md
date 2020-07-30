~~~
{
    "id": "how_to_annotate_a_traceroute_with_ixp",
    "name": "How to Annotate a Traceroute with IXP",
    "description": "The following solution will return a list of IXP names given IP addresses",
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
- Path to jsonl file of IXPs, which can be found here: [ixps dataset](https://www.caida.org/data/ixps/) under ixs_*.jsonl files
- List of IP addresses

**Usage:** `python3 ixp-annotations.py [path to jsonl file] [ip address] [ip address] ...`

i.e. `python3 ixp-annotations.py ixp.jsonl '198.32.231.77' '10'` will yield `['npIX PTS', None]`

~~~python

import json
import ipaddress

def annotate_traceroute(path, ips):
    """
    Inputs a path to data file and a list of IP addresses and returns a corresponding list of IXP names.
    """
    # Converts all into IP address format, appends None if not IP address
    ips_format = []
    for ip in ips:
        try:
            ips_format.append(ipaddress.ip_address(ip))
        except: 
            ips_format.append(None)
    final_set = [None]*len(ips)

    with open(path) as f:
        # skips first row (comment)
        next(f)
        for line in f:
            obj = json.loads(line)
            name = obj['name']
            recorded_ipv4 = list(map(ipaddress.ip_network, obj['prefixes']['ipv4']))
            recorded_ipv6 = list(map(ipaddress.ip_network, obj['prefixes']['ipv6']))
            for find in range(len(ips_format)):
                ele = ips_format[find]
                if ele != None:
                    # checks if ipv4 or ipv6
                    if ele.version == 4:
                        for ipv4 in recorded_ipv4:
                            if ele in ipv4:
                                final_set[find] = name
                    elif ele.version == 6:
                         for ipv6 in recorded_ipv6:
                            if ele in ipv6:
                                final_set[find] = name 
                    else:
                        continue                      
    print(final_set)
~~~

## Background

### What is an Internet Exchange Point (IXP)?
- An IXP is a physical infrastructure that allow Internet Service Providers (ISPs), Content Delivery Networks(CDNs), and other organizations to exchange Internet traffic between their networks
- [IXPs are managed by one of the following](https://www.internetsociety.org/issues/ixps/): non-profit organizations, associations of ISPs, operator-neutral for-profit companies, university or government agencies, informal associations of networks

### Caveats
- Assumes dataset contains valid IP addresses
