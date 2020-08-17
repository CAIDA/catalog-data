~~~
{
    "question": "How to find the origin ASN for a IPv4 address with Python?",
    "descriptions": "The following solution uses libipmeta's `PyIPMeta` to map between ipv4 addresses and origin asns."
    "links": [{"to":"software:pyipmeta"},{"to":"dataset:as_prefix"}],
    "id":"map_ipv4_address_to_asn",
    "name": "How to find the origin ASN for a IPv4 address with Python?",
    "descriptions": "The following solution uses libipmeta's `PyIPMeta` to map between ipv4 addresses and origin asns.",
    "links": ["software:pyipmeta"],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools",
        "asn",
        "ipv4",
        "ipv4 prefix"
    ]
}


### PyIPMeta ###

PyIPMeta is a Python library that provides a high-level interface for historical and realtime geolocation metadata lookups using Maxmind GeoIP and/or NetAcuity (Digital Element) geolocation databases.

#### Pre-requisites ####

Before installing PyIPMeta, you will need:\
• [libipmeta(>= 3.0.0)]( https://github.com/CAIDA/libipmeta)\
• Python setuptools (`sudo apt install python-setuptools` on Ubuntu) \
• Python development headers (`sudo apt install python-dev` on Ubuntu)

Detailed installation and usage instructions [here]( https://github.com/CAIDA/pyipmeta ).

# solution #

The following script returns a dictionary `ip2asn` that maps ips to origin asns. 

### Map between ips and origin asns using PyIPMeta ###

For this solution, clone **PyIPMeta** from [here]( https://github.com/CAIDA/pyipmeta)\
More data can be found at http://data.caida.org/datasets/routing/routeviews-prefix2as/

Sample ips.txt found [here]( http://data.caida.org/datasets/topology/ark/ipv4/dns-names/2019/05/dns-names.l7.20190501.txt.gz)

**Usage** : `$ python3 ip_asn.py -i ips.txt`

~~~python
import _pyipmeta 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest = 'ips_file', default = '', help = 'Please enter the file name of the ips file')
args = parser.parse_args()


ipm = _pyipmeta.IpMeta()

# print("Getting/enabling pfx2as provider (using included test data)")
prov = ipm.get_provider_by_name("pfx2as")
print(ipm.enable_provider(prov, "-f http://data.caida.org/datasets/routing/routeviews-prefix2as/2017/03/routeviews-rv2-20170329-0200.pfx2as.gz"))
print()

# Create list of ips from test file 
ips = []
with open(args.ips_file) as f:
    for line in f:
        line = line.rstrip().split("\t")[1]
        ips.append(line)


# Map between ipv4 addresses and origin asns
ip2asn = {}
for ip in ips:
    if ipm.lookup(ip):
        (res,) =  ipm.lookup(ip)
        if res.get('asns'):
            ip2asn[ip] = res.get('asns')[-1]


# print(ip2asn)
~~~

### <ins> Background </ins> ###

**What is an IPv4 address prefix?** \
• An *IP address* is a 32-bit unique address that is used to recognize a computer network or a machine. All computers on   the same data network share the same IP address.\
• An IPv4 address is typically written in decimal format as 4 8-bit fields separated by a period. Eg. 182.24.0.0/18 \
• An *IPv4 address prefix* is the prefix of an IPv4 address. \
• e.g. Consider the IPV4 address : 182.24.0.0/18 \
• In this case, 18 is the length of the prefix. \
• The prefix is the first 18 bits of the IP address. \
• More information on IPv4 addresses can be found [here]( https://docs.oracle.com/cd/E19455-01/806-0916/6ja85399u/index.html#:~:text=The%20IPv4%20address%20is%20a,bit%20fields%20separated%20by%20periods )

**What is forwarding/How does forwarding work?** \
• Fowarding means sending incoming information packets to the appropriate destination interface. This is done by routers with the help of a forwarding table. \
• Routers scan the destination IP prefix and locate a match using a forwarding table to determine the packet's next hop. \
• In cases of prefix overlap, where an incoming IP prefix map may match multiple IP entries in the table, the *Longest Prefix Matching Rule* is used to determine the next hop. 

**What is the Longest Prefix Matching Rule?** \
• Longest Prefix Match is an algorithm to lookup the destination an IP prefix’s next hop from the router. \
It finds the prefix matching the given IP address and returns the corresponding router node.\
• The router which corresponds to the IP address with the longest matching prefix is selected as the destination router node.\
• Consider the following example:
| IP Prefix        |   Router      |
| -------------    | ------------- |
| 192.168.20.16/28 | A             |
| 192.168.0.0/16   | B             |

• For example, for the given incoming IP address:  192.168.20.19 \
• **Node A** is selected as the destination router node as it contains the *longer matching prefix* i.e. 192.168.20.16 \
• Source: [link]( https://www.lewuathe.com/longest-prefix-match-with-trie-tree.html ) \
• More information can be found [here]( https://www.geeksforgeeks.org/longest-prefix-matching-in-routers/ )
 
**What is an AS?**\
 • AS stands for Autonomous system.\
 • It can be broadly be thought of as a single organization, or a collection of routers that route groups of IP addresses under a common administration, typically a large organization or an ISP (Internet Service Provider). \
 • It is a connected group of one or more IP addresses (known as IP prefixes) that provide a common way to route internet traffic to systems outside the AS.\
 • More information on AS can be found [here]( https://www.cs.rutgers.edu/~pxk/352/notes/autonomous_systems.html) and [here](https://www.caida.org/publications/presentations/2016/as_intro_topology_wind/as_intro_topology_wind.pdf)

### <ins> Caveats </ins> ###
• **Multi-origin AS** : Some prefixes originate from multiple AS's (which could be siblings or distinct organizations).\
This makes it more challenging to interpret the appearance of a matching destination IP address, as the address could be on a router operated by any one of the origin AS's.  \
• **Third-party AS's** \
• Border routers may use a third-party address when responding to traceroute probes. \
• A third-party address is an IP address corresponding to an AS that is not on the path toward a destination.

### <ins> Note: </ins> ###
• `pyasn` can also be used for mapping between ipv4 addresses and origin asns.\
• The `pyasn` object is be initialized using an IPASN datafile. \
• It also provides extremely fast lookups for IP addresses, as it returns the origin asns and the BGP prefixes it matches.\
• Detailed installation instructions and more information on Usage and IPASN data files [found here]( https://github.com/hadiasghari/pyasn ).\
• Note that the current `pyipmeta` **does not support** `ipv6`, whereas `pyasn` does. 

However, `pyipmeyta` provides **greater flexbility** as it provides the geographical information as well. 

For example, `ipm.lookup('192.172.226.97')` returns:

`[{'connection_speed': '', 'city': '', 'asn_ip_count': 0, 'post_code': '', 'lat_long': (37.750999450683594, -97.8219985961914), 'region': '', 'area_code': 0, 'asns': [], 'continent_code': 'NA', 'metro_code': 0, 'matched_ip_count': 1, 'region_code': 0, 'country_code': 'US', 'id': 223, 'polygon_ids': []}]`

• This object can then be parsed to map between IP addresses and origin asns. 

