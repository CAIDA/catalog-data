# How to find an asns customer cone

~~~json
{
    "id" : "how-to-find-an-asns-customer-cone",
    "visibility" : "public",
    "name" : "How to find an ASNs customer cone",
    "description" : "The following solution will help the user create a Python dictionary where the key is a given asn, and the values are the asn, it's customer cone, and customer cone size. This solution and script is usable for IPv4.",
    "links": [{"to":"dataset:as_relationships_serial_1"}],
    "tags" : [
        "ASN",
        "as relationships",
        "customer cone",
        "IPv4",
        "topology"
    ],
    "authors":[
        {
            "person": "person:wolfson__donald",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~
The following [script](as-customer-cone.py) produces a dictionary as_2_cone that maps an ASN to it's customer cone and size. The script has one flag: -p (.ppdc-ases) since you'll only need to provide a .ppdc-ases file in either a .txt or encoded .bz2 format.

~~~json
{
    "asn0" : {
        "asn" : "asn0",
        "cone" : [ "asn0", "asn1", "...", "asnM" ],
        "size" : 0
    },
}
~~~

### Usage

The dataset that is used for this script can be downloaded [here](https://www.caida.org/catalog/datasets/as-relationships/). Below is an example of running the script to get IPv4 customer cones from January 1, 2020. Reminder, this script can handle both .txt and .bz2 files.

~~~bash
python3 as-customer-cone.py -p 20200101.ppdc-ases.txt
~~~

Below is the helper method the script uses to parses the .ppdc-ases file line-by-line to update as_2_cone with a mapping between a given asn, its cone, and cone size.

~~~Python
# Given an line of a .ppdc-ases file, get the asn and its Customer Cone.
def parse_ppdc_ases_line(curr_line):
    global as_2_cone

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    customer_cone = curr_line.split()
    asn = int(customer_cone[0])
    customer_cone_size = len(customer_cone[1:])

    # Update as_2_cone with this asn's customer_cone_size.
    if asn not in as_2_cone:
        as_2_cone[asn] = {}

    as_2_cone[asn]["asn"] = asn
    as_2_cone[asn]["cone"] = customer_cone
    as_2_cone[asn]["size"] = customer_cone_size[1:]
~~~

## **<ins>Background</ins>**

### What is an AS

- AS stands for Autonomous system
- It can be broadly be thought of as a single organization, or a collection of routers that route groups of IP addresses under a common administration, typically a large organization or an ISP (Internet Service Provider).
- It is a connected group of one or more IP addresses (known as IP prefixes) that provide a common way to route internet traffic to systems outside the AS.
- Each AS is responsible for routing traffic within itself. This is known as intra-AS routing.
- Each AS can also route traffic between itself and other autonomous systems. This is known as inter-AS routing.
- More information on AS can be found [here]( https://www.cs.rutgers.edu/~pxk/352/notes/autonomous_systems.html) and [here](https://catalog.caida.org/details/media/2016_as_intro_topology_windas_intro_topology_wind.pdf)

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
- More information on AS Relationships can be found [here](https://www.caida.org/catalog/datasets/as-relationships/)

### What is a Customer Cone

- A customer cone is the set of ASes, prefixes, or addresses that can be reached from a given AS following only customer links.
- An AS A's AS customer cone as the AS A itself plus all the ASes that can be reached from A following only p2c links in BGP paths we observed.
  - In other words, A's customer cone contains A, plus A's customers, plus its customers' customers, and so on.
- The size of the customer cone of an AS reflects the number of other elements (ASes,  prefixes, or addresses) found in it's set.
- An AS in the customer cone is assumed to pay, directly or indirectly, for transit, and provides a coarse metric of the size or influence of an AS in the routing system.

### File Format: .ppdc-ases

For the purpose of this solution, we'll be skipping over any commented lines. Each line is a customer cone where asn0 is the "head" of the cone and all asns after is are within its cone.

~~~text
# inferred clique:

# total size: ...

<asn0>|<asn1>|...|<asnM>
~~~
