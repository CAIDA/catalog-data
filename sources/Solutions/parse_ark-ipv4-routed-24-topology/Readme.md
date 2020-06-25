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

https://www.caida.org/data/request_user_info_forms/ark.xml (download your copy of data)
https://docs.python.org/3/library/bz2.html

### Placeholder Nodes

Please port this Perl code into your Python script.
~~~Perl
# Many nodes in the ITDK are placeholder nodes.
# this are the non response hops in the traceroute
#   12.0.0.1  * 123.3.2.3
# We don't know what machine is there, but we know there is a machine between
# 12.0.0.1 and 123.3.2.3.
# In most analysis, we want to ignore placeholders.
# You identify placeholders by their IP addresses.
# Placeholder nodes have reserved IP addresses
# The following Perl code identifies placeholders

use constant MASK_3 => unpack("N",inet_aton("224.0.0.0"));
use constant PREFIX_224 => MASK_3;
use constant MASK_8 => unpack("N",inet_aton("255.0.0.0"));
use constant PREFIX_0 => unpack("N",inet_aton("0.0.0.0"));

my $not place_holder_node = 0;
foreach my $addr (split /\s+/, $addrs) {
    my $net = inet_aton($addr);
    my $binary = unpack("N", $net);
    if ((($binary & MASK_3) != PREFIX_224)
        && (($binary & MASK_3) != PREFIX_0)) {
        $not_placeholder_node = 1;
    }
}

// Only process the none placeholder nodes
if ($not_placeholder_node) {
    // Process Node, otherwise ignore it
}
~~~

### Nodes files

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
    "ips":["12.3.34"],
     "neighbors":[3,2,3],
    "location":{
        "continent":"SA",
        "country":"CO",
        "region":"34",
        "city"
        ....
     }
}
~~~

useage: parse_ark.py -n nodes.bz2 -l links.bz2 -a nodes.as.bz2 -g nodes.geo.bz2
~~~python
import argparse
import bz2

parser = argparse.ArgumentParser()
parser.add_argument('-n', dest = 'node_file', default = '', help = 'Please enter the file name of Nodes File')
parser.add_argument('-l', dest = 'link_file', default = '', help = 'Please enter the file name of Links File')
parser.add_argument('-a', dest = 'nodeas_file', default = '', help = 'Please enter the file name of Node-AS File')
parser.add_argument('-g', dest = 'geo_file', default = '', help = 'Please enter the file name of Node_Geolocation File')
args = parser.parse_args()


# file path of 4 files
dataset_dir = "../dataset/"
node_filePth = dataset_dir + args.node_file
link_filePth = dataset_dir + args.link_file
nodeas_filePth = dataset_dir + args.nodeas_file
geo_filePth = dataset_dir + args.geo_file

# create dictionary
nodes = {}

def node_lookup(nid):
	if nid not in nodes:
		node_id = nid.replace("N", "")
		nodes[nid] = {
			"id": node_id,
			"asn": "",
			"isp": [],
			"neighbor": [],
			"location": {
				"continent": "",
				"country": "",
				"region": "",
				"city": ""
				}
		}
	return nodes[nid]

# load nodes.bz2
print("open node file path:", node_filePth)
count = 0;
with bz2.open(node_filePth, mode='r') as f:
	for line in f:

		line = line.decode() #converting byte string to string

		# search the string with node in front
		if len(line) == 0 or line[0] == "#":
			continue

		#print(line)
		#print(line)
		value = line.strip(" \n") # remove tailing newline
		value = value.split(" ")
		#print(line)


		# get node id
		value[1] = value[1].replace(":", "")
		#value[1] = value[1].replace("N", "")
		node = node_lookup(value[1])
		
		# get isp
		for isp in value[2:]:
			if len(isp) != 0:
				node["isp"].append(isp)

		count += 1
		if count == 4:
			break

# load nodes.as.bz2
count = 0
print("node as file path:", node_filePth)
with bz2.open(nodeas_filePth, mode = 'r') as f:
	for line in f:
		line = line.decode()
		value = line.split(" ")

		node = node_lookup(value[1])
		node["asn"] = value[2]

		count += 1
		if count ==4:
			break
            
# load nodes.geo.bz2 file
count = 0
with bz2.open(geo_filePth, 'r') as f:
	for line in f:
		line = line.decode()

		# skip over comments
		if len(line) == 0 or line[0] == "#":
			continue

		value = line.split(" ")
		value[1] = value[1].split("\t")
		value[1][0] = value[1][0].replace(":", "")
		node = node_lookup(value[1][0])
		node["location"]["continent"] = value[1][1]
		node["location"]["country"] = value[1][2]
		node["location"]["region"] = value[1][3]
		node["location"]["city"] = value[1][4]

		count += 1
		if count == 1:
			break
            
# load links.bz2 file
count = 0
#print(nodes)
with bz2.open(link_filePth, 'r') as f:
	for line in f:
		line = line.decode()

		# skip over comments
		if len(line) == 0 or line[0] == "#":
			continue

		value = line.strip(" \n")
		value = value.split(" ")

		for nid in value[3:]:
			node = node_lookup(nid)
			for neighbor in value[3:]:
				if neighbor == nid:
					continue
				else:
					neighbor = neighbor.split(":")
					if node["neighbor"].count(neighbor[0]) == 0:
						node["neighbor"].append(neighbor[0])
		count += 1
		if count == 50:
			break

#print(nodes)


~~~
