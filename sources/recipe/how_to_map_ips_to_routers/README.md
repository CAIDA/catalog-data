~~~json
{
    "id": "how_to_map_ips_to_routers",
    "visibility":"public",
    "name": "How to infer which IPs belong to the same router.",
    "description": "Use bdrmapit to find out which set of IP addresses belong to the same router.",
    "tags": [
      "topology", 
      "routing", 
      "measurement methodology",
      "caida"
    ],
    "links": [
        "software:bdrmapit",
        "paper:2018_pushing_boundaries_bdrmapit",
        "dataset:ark_ipv4_traceroute"
    ],
    "authors":[
        {
            "person": "person:lee__isac",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## Introduction 
The following recipe provides an explanation of bdrmapIT as well as an in-depth walkthrough on running bdrmapIT on a collection of wart files to map IPs to routers. 

### Purpose: why map IPs to the same router?
Mapping IPs to the same router is crucial in understanding router-level topology and network ownership and boundaries. Mapping router ownership will faciliate research in interdomain congestion and the use of bdrmapIT can allow the creation for border mapping tools. These tools can assist in regulatory efforts, identify links between Internet networks, address network diagnostic challenges, and help estimate network traffic. 


## Background
Check [Pushing the Boundaries with bdrmapIT: Mapping Router
Ownership at Internet Scale](https://www.caida.org/catalog/papers/2018_pushing_boundaries_bdrmapit/pushing_boundaries_bdrmapit.pdf) for more in-depth details.
#### What is bdrmapIT used for? 
bdrmapIT helps map router ownership and network boundaries at a internet scale by combining two prior heuristics: bdrmap and MAP-IT. It tackles the challenge of inferring all AS-level network boundaries through a massive collection of traceroutes from various networks.
#### bdrmap
bdrmap used targeted traceroutes from a specific network, alias resolution probing techniques, and AS relationship inferences to infer the boundaries of that specific netowrk and the other networks attached at each boundary.
#### MAP-IT
MAPT-IT aggregates all available traceroute data
collected by many VPs in many ASes, but does not use any alias
resolution to infer routers.  
#### Why combine bdrmap and MAP-IT? 
bdrmap infers AS owners only for routers at the first AS boundary and requires a VP in each network of interest. MAP-IT lacks heurisitcs for edge networks and low-visibility links. 

<b>bdrmapIT addresses these issues and achieves greater accuracy and a more general solution to the challenge of researching Internet topology.</b>
#### Use Cases 
bdrmapIT can facilitate research in many domains, from interdomain congestion to resilience assessment, and help uncover bugs in network implementations. 

#### Definitions
* Trace Route: Is a network diagnostic tool used to track, in real-time, the pathway taken by a packet on an IP network from source to destination (reporting the IP addresses of all the routers it pinged in between). 
* AS Path: An AS path is the autonomous systems that routing information passed through to get to a specified router. 

## bdrmapIT installation
1. Create a new Python environment. Here we use Anaconda, but anything capable of creating and isolating a Python environment will work. 
```python
# Create new environment
conda create -n bdrmapit 'python<=3.9'
# Activate new environment
conda activate bdrmapit
```
2. Pip install bdrmapIT and dependencies. 
```python
# Install dependencies
pip install -U traceutils ip2as pb-amarder
# Install bdrmapIT
pip install -U bdrmapit
```
We also need to install scamper. However, scamper requires installation directly from the source code. 

* Download the source code [here](https://www.caida.org/catalog/software/scamper/).
* Run these lines. 
```python
./configure
make 
sudo make install
# Run line below only if on linux system. 
sudo ldconfig 
```
## Running bdrmapIT
1. <b>Create "Prefix to AS" mappings using ip2as.</b>

In order to do this, we must first download 5 files. 

* [Routeviews Prefix to AS Mappings Dataset](https://www.caida.org/catalog/datasets/routeviews-prefix2as/)
Navigate to directory: routeviews-prefix2as/
* [AS Relationships and AS Customer Cones](https://www.caida.org/catalog/datasets/as-relationships/)
Navigate to directory: /serial-1/*. Relationship files end with 'as-rel.txt.bz2' and cone files end in 'ppdc-ases.txt.bz2'.
* [AS-to-Organization Mappings](https://www.caida.org/catalog/datasets/as-organizations/)
* [PeeringDB](https://www.caida.org/catalog/datasets/peeringdb/)

To create the "Prefix to AS" mappings, run the following example:

```
ip2as -p routeviews-rv2-20211201-1200.pfx2as -P peeringdb_2_dump_2021_12_01.json -R 20211201.as-rel.txt.bz2 -c 20211201.ppdc-ases.txt.bz2 -a 20210401.as-org2info.jsonl.gz -o ip2as.prefixes
```
Refer to table below for command line arguments. 
| Argument      | Required | Description                                       |
|---------------|----------|---------------------------------------------------|
| p, -prefixes  | Required | RIB prefix to AS file.                            |
| P, -peeringdb | Required | PeeringDB json file                               |
| -R,--rels     | Required | AS relationships file retrieved from CAIDA.       |
| -c, --cone    | Required | AS customer cone file retrieved from CAIDA.       |
| -a, --as2org  | Required | AS-to-organization mappings retrieved from CAIDA. |
| -o, --output  | Optional | Output file. Defaults to stdout.                  |

2. <b>Download Wart Files and Run bdrmapIT.</b>

You can find the IPv4 traceroute wart files [here](https://www.caida.org/catalog/datasets/ipv4_routed_24_topology_dataset/). Scroll down to "Request Data Access", and choose the publicly available data. From there, navigate to ipv4/probe-data/. Choose the desired team and date traceroute files. 

Example of running bdrmapIT with 2 wart files:
```
bdrmapit all -i ip2as.prefixes -b as2org-file.gz -r rels-file.bz2 -c cone-file.bz2 -p 1 -W daily.l7.t2.c006946.20180829.acc-gh.warts.gz abz-uk.team-probing.c008972.20201201.warts.gz -k example
```
This line will output a file in the ITDK nodes.as format with 'example' as the file name.

Moreover, we can input the wart files as such: 
```python
# list of warts filenames, space separated
-W WFILELIST 
```

Run the following line to see all optional and required arguments: 
```
bdrmapit all -h
```

## Caveats

#### IPv4 Traceroute Files
Please look [here](https://publicdata.caida.org/datasets/topology/ark/ipv4/probe-data/README.txt) for more details on the data. 
* Team probing data is organized into lists and teams.  A list defines a
logical set of destinations. 
* A list does not necessarily mean a fixed set of destinations over time. It may be
merely a conceptual grouping of destinations according to some purpose,
goal, or technique. For example, list 7 is called allpref24, and the data
consists of traces to randomly selected destinations in every routed /24.
Thus, the set of destinations covered by list 7 changes every cycle, but
the list itself retains its conceptual identity. 

* There is no guarantee on the timeliness of daily files.
Daily files are meant for archiving, and thus are only created when all the
data making up a given daily file is fully available.  This means that the
creation of individual daily files can be subject to arbitrarily long delays
as a result of failures in the system.  This also means that a cycle
directory may be missing some daily files even though a subsequent cycle
directory exists.




Copyright (c) 2022 The Regents of the University of California
All Rights Reserved
