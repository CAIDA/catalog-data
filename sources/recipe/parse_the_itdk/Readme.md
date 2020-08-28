~~~json
{
    "id" : "parse_the_itdk",
    "visibility" : "public",
    "name": "Parse CAIDA's Internet Topology Data Kit (ITDK)",
    "description": "Parse the ITDK for an ASes', links, interfaces, and geographic location.",
    "links": [
        {
            "to": "dataset:internet-topology-data-kit"
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
    ]
}
~~~

## **<ins>Introduction</ins>**

This solution should help the user parse the Internet Topology Data Kit (ITDK) to map a node's ID to the ASN, its interfaces (IPs), links to other nodes (IP Layer links), and its geolocation.

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

## **<ins>Solution</ins>**

This solution has a [script](parse_itdk.py) which takes in four files and creates a dictionary, ```as_2_data``` which maps an AS to the data found in all files. The four files are a Nodes File (```-n```), Node-AS File (```-a```), Links File (```-l```), and a Node-Geolocation File (```-g```). The file also has an extra flag (```-p```) which takes in a comma sperated list of ASes which will have their data printed to STDOUT. 

To download the four files, you can access the data [here](https://www.caida.org/data/internet-topology-data-kit/). You'll need a .nodes, .nodes.as, nodes.geo, and a .links file. The script can handle both .bz2 and .txt file extensions so you don't need to decode the files.

The way the the script works is by first parsing the Nodes-AS file and mapping a ```node_id``` to its corresponding asn which is used in all other files. Next, the script parses the Links file to create objects in the dictionary ```as_2_data```, and updates each object with links to other ASes. Then the script parses the Nodes file which updates ```as_2_data```'s existing objects with interfaces found in the file. Finally, the script parses the Nodes-Geolocation file to update the existing objects in ```as_2_data``` with data found in the file.

### Usage

Below is an example of how to run the script, and print the AS 3356's data to STDOUT.

~~~bash
python3 parse_itdk.py -a midar-iff.nodes.as.bz2 -l midar-iff.links.txt -n midar-iff.nodes.txt -g midar-iff.nodes.geo.txt -p 3356
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

## **<ins>Background</ins>**

 - What is Internet Topology Data Kit (ITDK)?
   - The ITDK contains data about connectivity and routing gathered from a large cross-section of the global Internet. 
   - This dataset is useful for studying the topology of the Internet at the router-level, among other uses.
   - The Nodes File lists the set of interfaces that were inferred to be on each router.
   - The Links File lists the set of routers and router interfaces that were inferred to be sharing each link. Note that these are IP layer links, not physical cables or graph edges. More than two nodes can share the same IP link if the nodes are all connected to the same layer 2 switch (POS, ATM, Ethernet, etc).
   - The Node-AS file assigns an AS to each node found in the nodes file. We use our final bordermapIT assignment heuristic to infer the owner AS of each node.
   - The Node-Geolocation file contains the geographic location for each node in the nodes file. We use MaxMind's GeoLite City database for the geographic mapping.
   - More information can be found [here](https://www.caida.org/data/internet-topology-data-kit/)

### Format: Nodes File

~~~text
node <node_id>:   <i1>   <i2>   ...   <in>
~~~

### Format: Links File

~~~text
link <link_id>:   <N1>:i1   <N2>:i2   [<N3>:[i3]]   ..   [<Nm>:[im]]
~~~

### Format: Node-AS File

~~~text
node.AS   <node_id>   <AS>   <method>
~~~

### Format: Node-Geolocation File

~~~text
node.geo   <node_id>:   <continent>   <country>   <region>   <city>   <latitude>   <longitude>

node.geo   <node_id>:   <latitude>   <longitude>    <method>
~~~