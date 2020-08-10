~~~
{
    "id": "how_to_annotate_as_relationships_with_geographic_annotations",
    "visibility": "public",
    "name": "How to annotate as relationships with geographic annotations?",
    "description": "",
    "links": [{}],
    "tags": [
        "topology",
        "software/tools",
        "ASN",
        "geolocation",
        "country"
    ]
}
~~~
## **<ins> Introduction </ins>**

## **<ins> Solution </ins>**
Return the annotated AS relationship in the following format.
{
"asn0": {"asn1":[{"country":"US","city":"San Diego"},{"country":"US","city":"LA"}]},
"asn1": {"asn0":[{"country":"US","city":"San Diego"},{"country":"US","city":"LA"}]}
}
~~~python
def load_rel_geo(as_file, geo_file):

    re_format = re.compile("# format:(.+)")
    geo_info = {}

    with open(geo_file, 'r') as f:
        for line in f:
            m = re_format.search(line)
            if m:
                keys = m.group(1).strip().split("|")

            #skip comment of empty line
            if line[0] == "#" or len(line) == 0:
                continue

            line = line.strip().split("|")
            info={}
            for i in range(len(keys)):
                info[keys[i]] = line[i]

            if info['lid'] not in geo_info:
                geo_info[info['lid']] = info

    with open(as_file, 'r') as f:
        for line in f:
            if line[0] == "#" or len(line)==0:
                continue

            line = line.strip().split("|")
            if line[2]:
                source = geo_info[line[2].split(",")[0]]
            try:
                dest = geo_info[line[3].split(",")[0]]
            except:
                dest = {}

            as_rel_geo = {line[0]: {line[1]: [source, dest]}, line[1]: {line[0]: [source, dest]}}
            #print(as_rel_geo) 
~~~


 
##  **<ins> Background </ins>**

### What is an AS

- AS stands for Autonomous system
- It can be broadly be thought of as a single organization, or a collection of routers that route groups of IP addresses under a common administration, typically a large organization or an ISP (Internet Service Provider).
- It is a connected group of one or more IP addresses (known as IP prefixes) that provide a common way to route internet traffic to systems outside the AS.
- Each AS is responsible for routing traffic within itself. This is known as intra-AS routing.
- Each AS can also route traffic between itself and other autonomous systems. This is known as inter-AS routing.
- More information on AS can be found [here]( https://www.cs.rutgers.edu/~pxk/352/notes/autonomous_systems.html) and [here](https://www.caida.org/publications/presentations/2016/as_intro_topology_wind/as_intro_topology_wind.pdf)

### What is an ASN

- Each AS is assigned a unique ASN, or *Autonomous System Number* that allows it to be uniquely identified during routing.

### What is an AS Relationship

- An AS Relationship is the determined routing polocy between two ASes.
- The three most commo types of AS Relationships are:
  - customer-to-provider (c2p) (or if looked at from the opposite direction,  provider-to-customer p2c),
  - peer-to-peer (p2p),
  - sibling-to-sibling (s2s)
- A p2p link connect two ISPs who have agreed to exchange traffic between each other and their customer's. This can allow growing ISPs savings on transit costs compared to c2p relationships.
- An s2s link connects two ASes with a common administrative boundary. Such links usually appear as a result of mergers and acquisitions, or under certain network management scenarios.
- More information on AS Relationships can be found [here](https://www.caida.org/data/as-relationships/)


### Dataset ###
#### AS Relationships -- with geographic annotations
The Internet is composed of thousands of ISPs that operate individual parts of the Internet infrastructure. ISPs engage in both formal and informal relationships to collectively and ubiquitously route traffic in the Internet. These relationships turn into reality when two companies create physical connections between their networks, either by simply connecting two routers in a single location, or connecting pairs of routers in many different cities. Understanding the geographic nature of these relationships can facilitate activities such as: realistic simulation of AS path prediction; application performance estimation; predicting the likelihood that two ASes will interconnect; and visualizing the geographic distribution of networks.
More information and download dataset [here](https://www.caida.org/data/as-relationships-geo/)


### <ins> Caveats </ins>
