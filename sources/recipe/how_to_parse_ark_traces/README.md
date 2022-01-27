## How to parse through ark IPv4/IPv6 traceroutes
~~~json
{
    "id": "how_to_parse_ark_traces",
    "visibility": "public",
    "name": "How to parse through an ark traceroute?",
    "description": "This script parses an ark warts file using json to annotate a simple traceroute IP path.",
    "links": [{
        "to": "dataset:ipv4_prefix_probing_dataset",
        "to": "dataset:ipv4_routed_24_topology_dataset",
        "to": "dataset:ipv6_allpref_topology",
        "to": "dataset:ipv6_routed_48_topology_dataset"
        }],
    "tags": [
        "topology",
        "software/tools",
        "IPv4",
        "IPv4 prefix",
        "IPv6",
        "json",
        "parsing",
        "warts",
        "traceroute"
    ],
    "authors":[
        {
            "person": "zabegalin__sasha",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## Introduction
The solution parses traceroutes in ark warts file using json to annotate a simple traceroute IP path.

## Background 

### What is a Traceroute?
Traceroute is a computer network diagnostic command for displaying possible routes (paths) and measuring transit delays of packets across an Internet Protocol (IP) network.
More information can be found on [Wikipedia](https://en.wikipedia.org/wiki/Traceroute)

### What is Scamper?
Scamper is designed to actively probe destinations in the Internet in parallel (at a specified packets-per-second rate) so that bulk data can be collected in a timely fashion. 
Scamper's native output file format is called **warts**: a warts file contains substantial meta data surrounding each individual measurement conducted, as well as substantial detail of responses received. 

- More information on Scampper can be found [here](https://www.caida.org/catalog/software/scamper/) 
- Download source code from [here](https://www.caida.org/catalog/software/scamper/code/scamper-cvs-20200717.tar.gz) 
- Read Warts format in Python please read [pywarts](https://github.com/drakkar-lig/scamper-pywarts) 

### Dataset
#### IPv4 Prefix-Probing Traceroute Dataset
More information and download dataset [here](https://www.caida.org/catalog/datasets/ipv4_prefix_probing_dataset) 
Directory:` /datasets/topology/ark/ipv4/prefix-probing`

#### The IPv4 Routed /24 Topology Dataset
More information and download dataset [here](https://www.caida.org/catalog/datasets/ipv4_routed_24_topology_dataset) 
Directory: `/datasets/topology/ark/ipv4/probe-data`

#### Ark IPv6 Topology Dataset
More information and download dataset [here](https://www.caida.org/catalog/datasets/ipv6_allpref_topology_dataset) 
`Directory: /datasets/topology/ark/ipv6/probe-data`