~~~
{
    "id": "how_to_get_range_of_allocated_or_reserved_ips",
    "name": "How to get the range of allocated or reserved IPs?",
    "description": "The following solution will create two dictionaries listing the designations of IP addresses, one compressed without specific designations, one with designations.",
     "links": [{"to":"dataset:iana_ip_addresses"}]
    tags:[
      "ipv4", 
      "iana", 
      "ip address",
      "ip"
    ]
}
~~~

## Solution

This solution will return two dictionaries - one compressed (with only allocated, legacy, and reserved keys) and one with specific /8 IP designations. 

**Usage**: 

You can either enter a path to the current IANA IPv4 csv.

This link will download the latest available IPv4 space registry:
https://www.iana.org/assignments/ipv4-address-space/ipv4-address-space.csv

`python3 parse_ipv4.py [path to csv]`

~~~python
import pandas as pd
import sys
import more_itertools as mit

def parse_ip_assignees(csv_path):
    """
    Parses the IP address csv to ranges in which designations occupy. Takes in a path to the csv file and outputs a dictionary.
    """
    ip = pd.read_csv(csv_path).reset_index()
    ip["Designation"] = ip["Designation"].apply(lambda x: x.lower().replace("administered by", "").strip())

    consec = (lambda x: [list(group) for group in mit.consecutive_groups(list(x))])

    ip = (ip.drop(ip.columns.difference(["index","Designation"]), axis=1)
    .groupby(["Designation"])["index"]
    .apply(lambda x: [[y[0], y[-1]] for y in consec(x)])
    .to_dict())
    return ip

def parse_ip_compressed(csv_path):
    """
    Parses the IP address csv to ranges IP addresses are either reserved, allocated, or legacy. Takes in a path to the csv file and outputs a dictionary.
    """
    ip = pd.read_csv(csv_path).reset_index()
    ip["Status [1]"] == ip["Status [1]"].apply(lambda x: x.lower())

    consec = (lambda x: [list(group) for group in mit.consecutive_groups(list(x))])

    ip = (ip.drop(ip.columns.difference(["index","Status [1]"]), axis=1)
    .groupby(["Status [1]"])["index"]
    .apply(lambda x: [[y[0], y[-1]] for y in consec(x)])
    .to_dict())
    return ip

print(parse_ip_assignees(sys.argv[1]), parse_ip_compressed(sys.argv[1]))
 ~~~
 
 ## Background
 
 ### What is an IP address?
 
 - An IP address is a fundamental concept in the Internet Protocol
 - They are uniquely assigned labels assigned to devices in order route information to and from other devices in the network
 - Each IP address is 32-bits, separated into four 8-bit numbers
 
 ### What is a /8 address?
 
 - The first 8-bits of the IP address
 - Least specific; most /8 addresses are assigned to RIRs, or Regional Internet Registries, who allocate IP addresses to organizations in their respective regions
 
 ### What do the compressed designations mean?

 - **Legacy**: Either assigned to an organization or administered by an RIR. Legacy is used for blocks that have been assigned before the establishment of the RIRs.
 - **Allocated**: Allocated to an RIR
 - **Reserved**: Reserved for special purposes
 
 
 ## Caveats
 
 - This has been made specifically for the current IANA file
