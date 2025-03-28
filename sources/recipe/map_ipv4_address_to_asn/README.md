~~~json
{
  "name": "How to find the origin ASN for a IPv4 address with Python?",
  "description": "The following solution uses libipmeta's `PyIPMeta` to map between ipv4 addresses and origin asns.",
  "links": [
    {
      "to": "software:pyipmeta"
    },
    {
      "to": "dataset:routeviews_prefix2as"
    }
  ],
  "id": "map_ipv4_address_to_asn",
  "name": "How to find the origin ASN for a IPv4 address with Python?",
  "tags": [
    "measurement methodology",
    "topology",
    "software/tools",
    "asn",
    "ipv4",
    "ipv4 prefix"
  ],
  "authors":[
        {
            "person": "person:pathak__pooja",
            "organizations": [ "CAIDA, San Diego Supercomputer Center, University of California San Diego" ]
        },
        {
            "person": "person:carisimo__esteban",
            "organizations": [ "Northwestern University" ]
        }
    ]
}
~~~
### PyIPMeta

PyIPMeta is a Python library that provides a high-level interface for historical and realtime geolocation metadata lookups using Maxmind GeoIP and/or NetAcuity (Digital Element) geolocation databases.

#### Pre-requisites

Before installing PyIPMeta, you will need:
- [libipmeta(>= 3.0.0)]( https://github.com/CAIDA/libipmeta)
- Python setuptools (`sudo apt install python-setuptools` on Ubuntu) 
- Python development headers (`sudo apt install python-dev` on Ubuntu)

Detailed installation and usage instructions on the [PyIPMeta repo]( https://github.com/CAIDA/pyipmeta ).

# solution #

The code below serves as an example of how to use the IP to ASN Mapper tool to map a list of IP addresses to their respective Autonomous System Numbers (ASNs) using data from CAIDA's RouteViews prefix-to-AS snapshots. It demonstrates the integration with pandas for efficient data handling and showcases the tool's capability to perform historical analysis by utilizing a snapshot from a specific date.

### Variables to Be Modified by the User:
- **DataFrame Source**: Replace the example IP address list or the DataFrame initialization with loading your data from a CSV, JSON, or Parquet file. Use the commented code as a guide to load your data file.
- **date = `datetime.datetime(2020, 3, 4)**: Change this to the specific date for which you want to fetch the RouteViews prefix-to-AS snapshot. Ensure the format is datetime.datetime(YYYY, MM, DD).

### Map between IPs and origin ASNs using PyIPMeta

For this solution, clone **PyIPMeta** from the [PyIPMeta repo]( https://github.com/CAIDA/pyipmeta).

Download a prefix2asn file by following the directions on the [Routeviews Prefix-to-AS Mappings dataset page](https://catalog.caida.org/dataset/routeviews_prefix2as). When using the script, pass in the file name after the `-p` flag.

This script takes a list of IP addresses in the format used by CAIDA's [DNS Names dataset](https://catalog.caida.org/dataset/ark_ipv4_dns_names).

**Usage** : `$ python3 ip_asn_pyipmeta.py -p <pfx2as file> -i <ips txt file>`

~~~python
import _pyipmeta 
import argparse
import datetime
import os 
import psutil

def returnTime():
    return datetime.datetime.now()

def returnMemUsage():
    process = psutil.Process(os.getpid())
    return process.memory_info()[0]
    

ipm = _pyipmeta.IpMeta()
# print(ipm)

parser = argparse.ArgumentParser()
parser.add_argument('-p', dest = 'prefix2asn_file', default = '', help = 'Please enter the prefix2asn file name')
parser.add_argument('-i', dest = 'ips_file', default = '', help = 'Please enter the file name of the ips file')
args = parser.parse_args()

# print("Getting/enabling pfx2as provider (using included test data)")
prov = ipm.get_provider_by_name("pfx2as")
print(ipm.enable_provider(prov, f"-f {args.prefix2asn_file}"))
print()

# Create list of ips from test file
ips = []
with open(args.ips_file) as f:
    for line in f:
        line = line.rstrip().split("\t")[1]
        ips.append(line)

begin_time = returnTime()
begin_mem = returnMemUsage()  

# Map between ipv4 addresses and origin asns
ip2asn = {}
for ip in ips:
    if ipm.lookup(ip):
        (res,) =  ipm.lookup(ip)
        if res.get('asns'):
            ip2asn[ip] = res.get('asns')

print(ip2asn)
end_time = returnTime()
end_mem = returnMemUsage()

# hour:minute:second:microsecond
print("Delta time:" , end_time - begin_time)
print("Delta memory:", end_mem - begin_mem)
~~~

### Background

**What is an IPv4 address prefix?** 
- An *IP address* is a 32-bit unique address that is used to recognize a computer network or a machine. All computers on   the same data network share the same IP address.
- An IPv4 address is typically written in decimal format as 4 8-bit fields separated by a period. Eg. 182.24.0.0/18 
- An *IPv4 address prefix* is the prefix of an IPv4 address. 
- e.g. Consider the IPV4 address : 182.24.0.0/18 
- In this case, 18 is the length of the prefix. 
- The prefix is the first 18 bits of the IP address.

**What is forwarding/How does forwarding work?** 
- Fowarding means sending incoming information packets to the appropriate destination interface. This is done by routers with the help of a forwarding table. 
- Routers scan the destination IP prefix and locate a match using a forwarding table to determine the packet's next hop. 
- In cases of prefix overlap, where an incoming IP prefix map may match multiple IP entries in the table, the *Longest Prefix Matching Rule* is used to determine the next hop. 

**What is the Longest Prefix Matching Rule?** 
- Longest Prefix Match is an algorithm to lookup the destination an IP prefix’s next hop from the router. 
It finds the prefix matching the given IP address and returns the corresponding router node.
- The router which corresponds to the IP address with the longest matching prefix is selected as the destination router node.
- Consider the following example:
| IP Prefix        |   Router      |
| -------------    | ------------- |
| 192.168.20.16/28 | A             |
| 192.168.0.0/16   | B             |

- For example, for the given incoming IP address:  192.168.20.19 
- **Node A** is selected as the destination router node as it contains the *longer matching prefix* i.e. 192.168.20.16
- More information, from [GeeksforGeeks](https://www.geeksforgeeks.org/longest-prefix-matching-in-routers/ )
 
**What is an AS?**
- AS stands for Autonomous system.
- It can be broadly be thought of as a single organization, or a collection of routers that route groups of IP addresses under a common administration, typically a large organization or an ISP (Internet Service Provider). 
- It is a connected group of one or more IP addresses (known as IP prefixes) that provide a common way to route internet traffic to systems outside the AS.
- More information, from [Rutgers University](https://www.cs.rutgers.edu/~pxk/352/notes/autonomous_systems.html)

### Caveats
- **Multi-origin AS** : Some prefixes originate from multiple AS's (which could be siblings or distinct organizations).
This makes it more challenging to interpret the appearance of a matching destination IP address, as the address could be on a router operated by any one of the origin AS's.  
- **Third-party AS's** 
- Border routers may use a third-party address when responding to traceroute probes. 
- A third-party address is an IP address corresponding to an AS that is not on the path toward a destination.

### Note:
- `pyasn` can also be used for mapping between ipv4 addresses and origin asns.
- The `pyasn` object is be initialized using an IPASN datafile. 
- It also provides extremely fast lookups for IP addresses, as it returns the origin asns and the BGP prefixes it matches.
- Detailed installation instructions, more information on usage, and IPASN data files can be found on the [PyASN GitHub repo](https://github.com/hadiasghari/pyasn ).
- Note that the current `pyipmeta` **does not support** `ipv6`, whereas `pyasn` does. 

However, `pyipmeyta` provides **greater flexbility** as it provides the geographical information as well. 

For example, `ipm.lookup('192.172.226.97')` returns:

`[{'connection_speed': '', 'city': '', 'asn_ip_count': 0, 'post_code': '', 'lat_long': (37.750999450683594, -97.8219985961914), 'region': '', 'area_code': 0, 'asns': [], 'continent_code': 'NA', 'metro_code': 0, 'matched_ip_count': 1, 'region_code': 0, 'country_code': 'US', 'id': 223, 'polygon_ids': []}]`

- This object can then be parsed to map between IP addresses and origin asns. 



Copyright (c) 2024 The Regents of the University of California
All Rights Reserved
