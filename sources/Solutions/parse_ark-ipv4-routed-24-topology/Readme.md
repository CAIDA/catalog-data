~~~json
{
    "name": "How to get a router's IPs, ASN, neighbors, and geographic location.",
    "description":"Using the ASN's organizatoin's country in WHOIS to map an ASN to the country of it's headquarters.",
    "links": ["dataset:AS_Organization"],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools",
        "ASN",
        "geolocation"
    ]
}
~~~
https://www.caida.org/publications/papers/2012/topocompare-tr/topocompare-tr.pdf
https://www.caida.org/publications/presentations/2016/as_intro_topology_wind/as_intro_topology_wind.pdf
https://www.cs.rutgers.edu/~pxk/352/notes/autonomous_systems.html
https://www.caida.org/data/internet-topology-data-kit/ <--


https://docs.python.org/3/library/bz2.html

### Placeholder Nodes ###

Many nodes in the ITDK dataset are placeholder nodes. These are the non response hops in the traceroute. In most analysis, we want to ignore placeholder nodes. Placeholders have reserved IP addresses, so we identify them by thier IP addresses. In ITDK dataset, we use addresses `224.0.0.0` and `0.0.0.0` as the placeholder addresses. Placeholder nodes would not be put in the dictionay `nodes` in the solution.


Please port this Perl code into your Python script.
~~~Perl
#! A/opt/local/bin/perl
# Many nodes in the ITDK are placeholder nodes.
# this are the non response hops in the traceroute
#   12.0.0.1  * 123.3.2.3
# We don't know what machine is there, but we know there is a machine between
# 12.0.0.1 and 123.3.2.3.
# In most analysis, we want to ignore placeholders.
# You identify placeholders by their IP addresses.
# Placeholder nodes have reserved IP addresses
# The following Perl code identifies placeholders
use warnings;
use strict;

use Socket qw(PF_INET SOCK_STREAM pack_sockaddr_in inet_aton);


use constant MASK_3 => unpack("N",inet_aton("224.0.0.0"));
use constant PREFIX_224 => MASK_3;
use constant MASK_8 => unpack("N",inet_aton("255.0.0.0"));
use constant PREFIX_0 => unpack("N",inet_aton("0.0.0.0"));

my $nodes_total = 0;
my $placeholder_total = 0;

while (<>) {
    next if (/#/);
    my ($node,$nid,@addrs) = split /\s+/;
    my $placeholder;
    foreach my $addr (@addrs) {
        my $net = inet_aton($addr);
        my $binary = unpack("N", $net);
        if ((($binary & MASK_3) == PREFIX_224)
            || (($binary & MASK_8) == PREFIX_0)) {
            $placeholder = 1;
            last;
        }
    }
    if (not $placeholder) {
        $nodes_total += 1;
    } else {
        $placeholder_total += 1;
    }

    #print ("$not_place_holder_node $nodes_total $placeholder_total\n");
    # Only process the none placeholder nodes
    #last if ($nodes_total > 10);
}

print ("nodes_total: ",$nodes_total,"\n");
print ("placeholder: ",$placeholder_total,"\n");
~~~

### Explanation of the data fields ###
*ITDK Datasets:* [link](https://www.caida.org/data/request_user_info_forms/ark.xml)

midar-iff.nodes.bz2
~~~
node N1:  5.2.116.4 5.2.116.28 5.2.116.66 5.2.116.70 5.2.116.78 5.2.116.88 5.2.116.108 5.2.116.142
~~~

midar-iff.links.bz2
~~~
link L1:  N27677807:1.0.0.1 N106961
~~~

midar-iff.nodes.as.bz2
~~~
node.AS N1 31655 refinement
~~~

midar-iff.nodes.geo.bz
~~~
# node.geo nod_id: continent country region city lat lon population method
node.geo N4:    SA      CO      34      Bogota  4.60971 -74.08175       7674366         ddec
~~~

ecode
~~~json
{
    "id":4,
    "asn":123,
    "isp":["12.3.34"],
     "neighbors":{"3,2,3"},
    "location":{
        "continent":"SA",
        "country":"CO",
        "region":"34",
        "city": "Bogota"
     }
}
~~~


### Solution ###
The following script returns a dictionary `nodes` that parse the data from 4 Nodes Files, nodes.bz2, links.bz2, nodes.as.bz2 and nodes.geo.bz2 in the following format:\
{'N12285': {`id`: ' ', `asn`: ' ', `isp`: [], `neighbor`: {}, `location`: { `continent`: ' ', `country`: ' ', `region`: ' ', `city`: ' '}}

useage: parse_ark.py -n nodes.bz2 -l links.bz2 -a nodes.as.bz2 -g nodes.geo.bz2

~~~python
import argparse
import bz2
import socket
import struct

parser = argparse.ArgumentParser()
parser.add_argument('-n', dest = 'node_file', default = '', help = 'Please enter the file name of Nodes File')
parser.add_argument('-l', dest = 'link_file', default = '', help = 'Please enter the file name of Links File')
parser.add_argument('-a', dest = 'nodeas_file', default = '', help = 'Please enter the file name of Node-AS File')
parser.add_argument('-g', dest = 'geo_file', default = '', help = 'Please enter the file name of Node_Geolocation File')
args = parser.parse_args()

# create dictionary
nodes = {}
MASK_8 = struct.unpack("!I", socket.inet_aton("255.0.0.0"))[0]
PREFIX_224 = struct.unpack("!I", socket.inet_aton("224.0.0.0"))[0]
MASK_3 = PREFIX_224
PREFIX_0 = struct.unpack("!I", socket.inet_aton("0.0.0.0"))[0]

def node_lookup(nid):
    """
    To check whether nid is in the ndoes.
    If not, create one in nodes.

    param: string, input node id
    """
    if nid not in nodes:
        #node_id = nid.replace("N", "")
        nodes[nid] = {
            "id": node_id,
            "asn": "",
            "isp": [],
            "neighbor": set(),
            "location": {
                "continent": "",
                "country": "",
                "region": "",
                "city": ""
                }
        }
    return nodes[nid]

def placeholder_lookup(addr):
    """
    To check whether the node is a placeholder or not
    If the addr is in 224.0.0.0 or 0.0.0.0, then it is a placeholder

    param:
    addr: string, input IPv4 addresss
    """
    binary_addr = struct.unpack("!I", socket.inet_aton(addr))[0]

    if (binary_addr & MASK_3) != PREFIX_224 and (binary_addr & MASK_8) != PREFIX_0:    
        return False
    else:
        return True

# === load nodes.bz2 ===
with bz2.open(args.node_file, mode='r') as f:

    for line in f:
    
        # convert byte string to string
        line = line.decode() 

        # skip the comments or the length of line is zero
        if len(line) == 0 or line[0] == "#":
            continue

        value = line.strip(" \n") # remove tailing newline
        value = value.split(" ")
        value[1] = value[1].replace(":", "") # value[1] == nid
             
        # get isp and check whether the node is placeholder
        isp_list = []
        placeholder = False

        for isp in value[2:]:
            if len(isp) == 0:
                continue
            if placeholder_lookup(isp):
                placeholder = True           
            isp_list.append(isp)

        # if the node the not placeholder, then process the node
        if not placeholder:
            node = node_lookup(value[1])
            node['id'] = value[1].replace("N", "")
            node['isp'] = isp_list

# === load nodes.as.bz2 ===
with bz2.open(args.nodeas_file, mode = 'r') as f:
    for line in f:
        line = line.decode()
        value = line.split(" ")

        # if the node is in nodes, assign AS number to each node
        if value[1] in nodes:
            nodes[value[1]]["asn"] = value[2]

# === load nodes.geo.bz2 file ===
with bz2.open(args.geo_file, 'r') as f:
    for line in f:
        line = line.decode()

        # skip over comments
        if len(line) == 0 or line[0] == "#":
            continue

        value = line.split(" ")
        value[1] = value[1].split("\t")
        value[1][0] = value[1][0].replace(":", "")

        # if the node is in nodes, assign geo info to each node
        if value[1][0] in nodes:
            node = nodes[value[1][0]]
            node["location"]["continent"] = value[1][1]
            node["location"]["country"] = value[1][2]
            node["location"]["region"] = value[1][3]
            node["location"]["city"] = value[1][4]     

# === load links.bz2 file ===
with bz2.open(args.link_file, 'r') as f:
    for line in f:
        line = line.decode()

        # skip over comments of the length of line is zero
        if len(line) == 0 or line[0] == "#":
            continue

        value = line.strip(" \n")
        value = value.split(" ")
    
        neighbors = []
        for nid in value[3:]:
            neighbors.append(nid.split(":")[0])

        for nid in neighbors:
            if nid in nodes:
                for n in neighbors:
                
                    #skip its neighbors are the node itself 
                    if nid == n or n not in nodes:
                        continue

                    nodes[nid]["neighbor"].add(n)
                    nodes[n]["neighbor"].add(nid)
~~~
