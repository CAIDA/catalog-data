~~~json
{
    "id" : "how_to_parse_ipv6_dns_name",
    "name": "How to Parse IPv6 DNS Names Dataset)",
    "description":"The following solution will help the user parse IPv6 DNS Names into a mapping between ip addresses and their hostnames.",

    "links": [
        {
            "to": "dataset:ark_ipv6_dns_names"
        }
    ],
    "tags": [
        "ipv6",
        "ip",
        "dns",
        "hostname"
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

This recipe should show the user how to parse a given IPv6 DNS Names file to map an ip address to its respective hostname. This recipe comes with the following [script](https://github.com/CAIDA/catalog-data/blob/how_to_parse_ipv6_dns_names/sources/recipe/how_to_parse_ipv6_dns_names/ip_2_hostname.py) which has the code to handle this solution. Code snippets below show key features of the code that are most usefull. The script has two flags, `-d` which is a path to a DNS Names file, and `-i` which is an optional comma seperated list of ip address. The ip addresses given in the `-i` flag will have their hostnames printed to STDOUT if possible.

## Solution

For this solution, you will need to download a IPv6 DNS Names file from CAIDA's website which can be done [here](https://www.caida.org/catalog/datasets/ipv6_dnsnames_dataset).

### Usage

Below is an example of how to run the code, and get the the hostsnames of the two listed ip addresses. This script can handle both encoded .gz files and generic .txt files, so you don't have to decode the file prior to running the script.

~~~bash
python3 ip_2_hostname.py -d dns-names.l8.20200101.txt -i 2001:5a0:2000:500::1,2001:5a0:2000:400::44
~~~

### Parsing DNS Names File Line-By-Line

~~~Python
# Given a line of a DNS Names File, map each line's ip address to its hostname.
def parse_dns_names_line(curr_line):
    global ip_2_hostname

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    # Try to pull all the data out of the current line.
    try:
        timestamp, ip_address, router_name = curr_line.split()
        
        # Map the current ip address to its hostname.
        ip_2_hostname[ip_address] = router_name
    except:
        pass    # Do nothing. Likely caused by a line missing all three columns.
~~~

### Print a Given IP Addresses Hostname

~~~Python
# Helper method to print a hostname for a given ip address.
def print_hostname(ip_address):
    global ip_2_hostname

    if ip_address in ip_2_hostname:
        hostname = ip_2_hostname[ip_address]
        print("IP Address: {}, Hostname: {}".format(ip_address, hostname))
    else:
        print("No hostname found for: {}".format(ip_address))
~~~

## Background

- What is the IPv6 DNS Name Dataset?
  - The IPv6 DNS Names dataset provides fully-qualified domain names for IPv6 addresses seen in the traces of the IPv6 Topology Dataset.
- What is DNS Names Dataset used for?
  - DNS names are useful for obtaining additional information about routers and hosts making up the Internet topology. 
    - For example, DNS names of routers often encode the link type: backbone vs. access, link capacity, Point of Presence (PoP), and geographic location.

### DNS Names File Format:

We are assuming each line is within this format, the provided script skips any commented line (lines starting with '#'), and skips any line that isn't three variables long.

~~~Text
<timestamp> <ip_address> <hostname>
~~~

### Caveats

CAIDA performs DNS lookups centrally at CAIDA using a custom-built bulk DNS lookup service. This service performs millions of DNS lookups per day. In general, CAIDA performs DNS lookups soon after collecting the topology traces so that the results better match the state of the Internet at trace collection time. However, to avoid undue load on remote DNS nameservers and to keep the daily lookup volume at a manageable level, CAIDA never performs a lookup for an address if it's successfully obtained a result in the preceding 36 hours. Apart from this 36-hour rule, we always perform a lookup whenever we encounter an IP address in traces. This means that CAIDA doesn't repeat lookups at 36-hour granularity for addresses that repeatedly occur in the traces.


Copyright (c) 2020 The Regents of the University of California
All Rights Reserved