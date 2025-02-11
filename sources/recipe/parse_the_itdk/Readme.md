~~~json
{
    "id" : "parse_the_itdk",
    "name": "Parse CAIDA's ITDK for a router's IPs, ASN, neighbors, and geographic location.",
    "description":" The following solution will help the user create a Python dictionary that contains a router's IPs, ASN, neighbors, and geographic location",

    "links": [
        {
            "to": "dataset:ark_itdk"
        }
    ],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools",
        "ASN",
        "geolocation",
        "link",
        "node_id"
    ],
    "authors":[
        {
            "person": "person:lu__louis",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        },
        {
            "person": "person:wolfson__donald",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~


## Introduction

This solution parses through ITDK datasets and stores a node's `node id`, `asn` and `location` as a json object. 
The relevant `node` information is extracted from 4 different files: 
- `node id` from **nodes.bz2** 
- `asn` from **nodes.as.bz2** 
- `neighbors` from **links.bz2** 
- `location` from **nodes.geo.bz2**


## Solution

This solution has a [script](parse_itdk.py) which takes in four files and creates a dictionary, ```as_2_data``` which maps an AS to the data found in all files. The four files are a Nodes File (```-n```), Node-AS File (```-a```), Links File (```-l```), and a Node-Geolocation File (```-g```). The file also has an extra flag (```-p```) which takes in a comma sperated list of ASes which will have their data printed to STDOUT. 

To download the four files, you can access the data [here](https://www.caida.org/catalog/datasets/internet-topology-data-kit/). You'll need a .nodes, .nodes.as, nodes.geo, and a .links file. The script can handle both .bz2 and .txt file extensions so you don't need to decode the files.

The way the the script works is by first parsing the Nodes-AS file and mapping a ```node_id``` to its corresponding asn which is used in all other files. Next, the script parses the Links file to create objects in the dictionary ```as_2_data```, and updates each object with links to other ASes. Then the script parses the Nodes file which updates ```as_2_data```'s existing objects with interfaces found in the file. Finally, the script parses the Nodes-Geolocation file to update the existing objects in ```as_2_data``` with data found in the file.

~~~json
{
    "asn" : {
        "asn" : "...",
        "links" : {},
        "interfaces" : {},
        "continent" : "...",
        "country" : "...",
        "region" : "...",
        "city" : "...",
        "latitude" : "...",
        "longitude" : "..."
    }
}
~~~

### Usage

Below is an example of how to run the script, and print the AS 3356's data to STDOUT.

~~~bash
python3 parse_itdk.py -a midar-iff.nodes.as.bz2 -l midar-iff.links.txt -n midar-iff.nodes.txt -g midar-iff.nodes.geo.txt -p 3356
~~~


### Placeholder Perl Code 
This Perl code parse nodes.bz2 file only and identify the placeholder nodes.
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

### Parsing the Nodes-AS file, and map node_ids to ASes:

~~~Python
# Parses a given line of the nodes_as_file and updates as_2_data.
def parse_nodes_as_body(curr_line):
    global node_id_2_asn

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    # Format of curr_line: "node.AS   <node_id>   <AS>   <method>"
    ignore, node_id, asn, method = curr_line.split()

    # Map the node_id to its corresponding asn.
    node_id_2_asn[node_id] = asn
~~~

### Parsing the Links file, and create AS objects, and updating links:

~~~Python
# Given a string of a line from a Links File, update as_2_data.
def parse_links_body(curr_line):
    global as_2_data
    global node_id_2_asn

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    # Format of curr_line: "link <link_id>: <N1>:i1 <N2>:i2 [ <N3>:[i3] ... ]"
    curr_line = curr_line.split()
    
    # Skip any lines that don't have any data.
    if len(curr_line) < 4:
        return

    # Format of curr_line: [ "link", link_id, [ N1, Interface ], N2, ... ]
    curr_line[2] = curr_line[2].split(":")
    node_id = curr_line[2][0]
    
    # Edge Case: Skip this line if the node_id doesn'st map to an asn.
    if node_id in node_id_2_asn:
        asn = node_id_2_asn[curr_line[2][0]]
    else:
        return
    
    # Create the current asn's object.
    as_2_data[asn] = {
        "asn" : asn,
        "links" : set(),
        "interfaces" : set(),
        "continent" : None,
        "country" : None,
        "region" : None,
        "city" : None,
        "latitude" : None,
        "longitude" : None
    }

    # Add the current interface if it exists.
    if len(curr_line[2]) == 2:
        interface = curr_line[2][1]
        as_2_data[asn]["interfaces"].add(interface)

    # Iterate over N2 to Nm and all add asns to the current link interface.
    for node in curr_line[3:]:
        # Split the node_id from the interface.
        node_data = node.split(":")
        node_id = node_data[0]
        
        # Add the link between the asn and node if the node has a mappable asn.
        if node_id in node_id_2_asn:
            curr_asn = node_id_2_asn[node_id]

            # Add the current asn to the parent asn's links set.
            as_2_data[asn]["links"].add(curr_asn)
~~~

### Parsing the Nodes file, and updating each object with its interfaces:

~~~Python
# Parses a given line of the nodes_file and updates as_2_data.
def parse_nodes_body(curr_line):
    global as_2_data
    global node_id_2_asn
    
    # Edge Case: Skip any commented lines. 
    if curr_line == "#":
        return

    # Format of curr_line: "node <node_id>: <i1> <i2> ... <in>"
    curr_line = curr_line.split()
    # Format of curr_line: [ "node", "<node_id>:", "<i1>", "<i2>", ..., "<in>" ]
    node_id = curr_line[2].replace(":","")

    # Skip line if node_id isn't mappable to an asn.
    if node_id not in node_id_2_asn:
        return

    asn = node_id_2_asn[node_id]

    # Skip line if asn not in as_2_data.
    if asn not in as_2_data:
        return

    # Iterate over interfaces on the current line, and add them to as_2_data.
    for interface in curr_line[2:]:
        as_2_data[asn]["interfaces"].add(interface)
~~~

### Parsing the Nodes-Geolocation, and updating objects with geolocations:

~~~Python
# Parses a given line of the nodes_geo_file and updates as_2_data.
def parse_nodes_geo_body(curr_line):
    global as_2_data
    global node_id_2_asn

    # Edge Case: Skip any commented lines. 
    if curr_line == "#":
        return
    
    curr_line = curr_line.split()
    node_id = curr_line[1].replace(":","")

    # Skip line if node_id isn't mappable to an asn.
    if node_id not in node_id_2_asn:
        return

    asn = node_id_2_asn[node_id]

    # Skip line if asn not in as_2_data.
    if asn not in as_2_data:
        return

    # Depending on length of curr_line update data with what is given.
    if len(curr_line) == 8:
        as_2_data[asn]["continent"] = curr_line[2]
        as_2_data[asn]["country"] = curr_line[3]
        as_2_data[asn]["region"] = curr_line[4]
        as_2_data[asn]["city"] = curr_line[5]
        as_2_data[asn]["latitude"] = curr_line[6]
        as_2_data[asn]["longitude"] = curr_line[7]
    elif len(curr_line) == 5:
        as_2_data[asn]["latitude"] = curr_line[2]
        as_2_data[asn]["longitude"] = curr_line[3]
~~~

### Helper method for printing ASes to STDOUT:

~~~Python
# Print a given asn to STDOUT.
def get_as_data(asn):
    global as_2_data
    
    # Edge Case: Print error if asn not in as_2_data.
    if asn not in as_2_data:
        print("{} not in as_2_data".format(asn))
    else:
        print(as_2_data[asn])
~~~

## Background

 - What is Internet Topology Data Kit (ITDK)?
   - The ITDK contains data about connectivity and routing gathered from a large cross-section of the global Internet. 
   - This dataset is useful for studying the topology of the Internet at the router-level, among other uses.
   - The Nodes File lists the set of interfaces that were inferred to be on each router.
   - The Links File lists the set of routers and router interfaces that were inferred to be sharing each link. Note that these are IP layer links, not physical cables or graph edges. More than two nodes can share the same IP link if the nodes are all connected to the same layer 2 switch (POS, ATM, Ethernet, etc).
   - The Node-AS file assigns an AS to each node found in the nodes file. We use our final bordermapIT assignment heuristic to infer the owner AS of each node.
   - The Node-Geolocation file contains the geographic location for each node in the nodes file. We use MaxMind's GeoLite City database for the geographic mapping.
   - More information can be found [here](https://www.caida.org/catalog/datasets/internet-topology-data-kit/)

### Explanation of the Data Files 
*Download ITDK Datasets:* [link](https://www.caida.org/catalog/datasets/request_user_info_forms/ark)
The datasets are located in `ark/ipv4/itdk`

#### midar-iff.nodes.bz2
The nodes file lists the set of interfaces that were inferred to be on each router. 
Each line indicates that a node `node_id` has interfaces i<sub>1</sub> to i<sub>n</sub>.


**File format**: node &lt;node_id&gt;: &nbsp; &lt;i<sub>1</sub>&gt; &nbsp; &lt;i<sub>2</sub>&gt; &nbsp; ... &nbsp; &lt;i<sub>n</sub>&gt; 

~~~
node N1:  5.2.116.4 5.2.116.28 5.2.116.66 5.2.116.70 5.2.116.78 5.2.116.88 5.2.116.108 5.2.116.142
~~~

#### midar-iff.links.bz2
The links file lists the set of routers and router interfaces that were inferred to be sharing each link. 
Each line indicates that a link `link_id` connects nodes N<sub>1</sub> to N<sub>m</sub>. 
If it is known which router interface is connected to the link, then the interface address is given after the node ID separated by a colon.


**File format**: link &lt;link_id&gt;: &nbsp; &lt;N<sub>1</sub>&gt;:i<sub>1</sub> &nbsp;  &lt;N<sub>2</sub>&gt;:i<sub>2</sub> &nbsp;  &lt;N<sub>3</sub>&gt;:i<sub>3</sub> &nbsp;  ... &nbsp;  &lt;N<sub>m</sub>&gt;:i<sub>m</sub>

~~~
link L1: N27677807:1.0.0.1 N106961
~~~

#### midar-iff.nodes.as.bz2
The node-AS file assigns an AS number to each node found in the nodes file.


**File format**: node.AS   &lt;node_id&gt;   &lt;AS&gt;   &lt;method&gt;
~~~
node.AS N1 31655 refinement
~~~

#### midar-iff.nodes.geo.bz
The node-geolocation file contains the geographic location for each node in the nodes file.


**File format**: node.geo   &lt;node_id&gt;:   &lt;continent&gt;   &lt;country&gt;   &lt;region&gt;   &lt;city&gt;   &lt;latitude&gt;   &lt;longitude&gt;
~~~
node.geo N4: SA CO 34 Bogota 4.60971 -74.08175       
~~~
    
More information on ITDK dataset can be found [here](https://www.caida.org/catalog/datasets/internet-topology-data-kit/)

### Caveats

- Placeholder nodes are the non-response hops in the traceroute. 
- Generally, placeholder nodes are ignored. 
- Placeholder nodes have reserved IP addresses used to identify them. For the ITDK dataset, we use addresses `224.0.0.0` and `0.0.0.0` as the placeholder addresses.


Copyright (c) 2020 The Regents of the University of California
All Rights Reserved