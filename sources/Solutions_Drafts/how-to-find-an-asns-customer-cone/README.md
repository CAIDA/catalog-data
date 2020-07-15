# How to find an asns customer cone

~~~json
{
    "id" : "solution:how-to-find-an-asns-customer-cone",
    "visibility" : "public",
    "name" : "How to find an asns customer cone",
    "description" : "Using a .as-rel, and .paths file to get each provided asn's customer cone.",
    "links" : [{"to":""}],
    "tags" : [
        "ASN",
        "as-rel",
        "Customer Cone",
        "IPv4",
        "IPv6",
        "paths",
        "Topology"
    ]
}
~~~

## **<ins>Introduction</ins>**

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

### What is a Customer Cone

- A customer cone is the set of ASes, prefixes, or addresses that can be reached from a given AS following only customer links.
- An AS A's AS customer cone as the AS A itself plus all the ASes that can be reached from A following only p2c links in BGP paths we observed.
  - In other words, A's customer cone contains A, plus A's customers, plus its customers' customers, and so on.
- The size of the customer cone of an AS reflects the number of other elements (ASes,  prefixes, or addresses) found in it's set.
- An AS in the customer cone is assumed to pay, directly or indirectly, for transit, and provides a coarse metric of the size or influence of an AS in the routing system.

## **<ins>Caveats</ins>**

Getting the customer cone for IPv4 asns is less work than IPv6. The file forrmat, .ppdc-ases is already the a file that provides the customer cone of a given asn. The format of this file is below. However, for IPv6, you'll need to map AS Relationships to a Paths file.

## **<ins>Solution</ins>**

The following [script](as-customer-cone.py) produces a dictionary as_2_cone that maps an ASN to it's customer cone or size. The script has three possible flags: -p (.ppdc-ases), -r (.as-rel.v6-stable), and -P (.stable.paths6). For IPv4, you'll only need to provide a .ppdc-ases file in either a .txt or encoded .bz2 format. For IPv6, you'll need to provide .as-rel.v6-stable and .stable.paths6 file. Both of must be in either .txt or encoded .bz2 formats.

~~~json
{
    "<asn0>" : {
        "asn" : <asn0>,
        "cone" : [ <asn0>, <asn1>, ..., <asnM> ],
        "size" : #
    },
}
~~~

Below is an example of running the script to get IPv4 customer cones from January 1, 2020.

~~~bash
python3 as-customer-cone.py -p /data/external/as-rank-ribs/20200101/20200101.ppdc-ases.txt.bz2
~~~

Below is an example of running the script to get IPv6 customer cones from January 1, 2020.

~~~bash
python3 as-customer-cone.py -P /data/external/as-rank-ribs/20200101/20200101.stable.paths6.bz2 -r /data/external/as-rank-ribs/20200101/20200101.as-rel.v6-stable.txt.bz2
~~~

## **<ins>File Formats and Code Snippets</ins>**

### File Format: .as-rel.v6-stable

For the purpose of this solution, we'll be skipping over any commented lines since we do not need the BGP monitors.

~~~text
# source:topology|BGP|<data>|<system>|<monitor>
<asn0>|<asn1>|<relationship>
~~~

Below is an example of the possible formats of AS Relationships.

~~~text
<asn0>|<asn1>|-1    <asn1> is a customer of <asn0>
<asn0>|<asn1>|0     <asn1> is a peer of <asn0>
<asn0>|<asn1>|1     <asn1> is a provider of <asn0>
~~~

Below is a how the script parses this type of file's lines to create a mapping between two asns and their relationship:

~~~Python
global as_pair_2_rel

# Edge Case: Skip any commented lines.
if curr_line[0] == "#":
    return

as_rel_set = curr_line.split("|")

# Get each piece of data from the current line.
asn0 = as_rel_set[0]
asn1 = as_rel_set[1]
relationship = int(as_rel_set[2])

# Place both related AS's in as_pair_2_rel based value of AS.
if (asn0 > asn1):
    temp = asn0
    asn0 = asn1
    asn1 = temp
    relationship = -1 * relationship

key = asn0 + " " + asn1

# Add the pair's relationship if doesn't already exist.
if key not in as_pair_2_rel:
    as_pair_2_rel[key] = relationship
~~~

### File Format: .ppdc-ases

For the purpose of this solution, we'll be skipping over any commented lines.

~~~text
# inferred clique:

# total size: ...

<asn0>|<asn1>|...|<asnM>
~~~

Below is a how the script parses this type of file's lines to update as_2_cone with a mapping between a given asn, its cone, and cone size.

~~~Python
global as_2_cone
global as_pair_2_rel

# Edge Case: Skip any commented lines.
if curr_line[0] == "#":
    return

asns = curr_line.rstrip().split("|")
for i in range(0, len(asns)):
    asn = int(asns[i])

# Map the current asn if the asn is not in as_2_cone yet.
if asn not in as_2_cone:
    as_2_cone[asn] = {}
    as_2_cone[asn]["asn"] = asn
    as_2_cone[asn]["cone"] = [asn]
    as_2_cone[asn]["size"] = 1

    # Compare asns[i] to each asn that comes after it.
    for j in range(i + 1, len(asns)):
        # Call helper function to format key to have asn's sorted by value.
        key = format_key(asn, int(asns[j]))

        # Add asns with a "provider" relationship between: asn[i] asn[j]
        if key in as_pair_2_rel and as_pair_2_rel[key] == 1:
            as_2_cone[asn]["size"] += 1
            as_2_cone[asn]["cone"].append(int(asns[j]))
        else:
            break  
~~~

### File Format: .stable.paths6

For the purpose of this solution, we'll be skipping over any commented lines since we do not need the BGP monitors.

~~~text
# source:topology|BGP|<data>|<system>|<monitor>
<asn0>|<asn1>|...|<asnM>
~~~

Below is a how the script parses this type of file's lines to update as_2_cone with a mapping between a given asn, its cone, and cone size.

~~~Python
global as_2_cone
global as_pair_2_rel

# Edge Case: Skip any commented lines.
if curr_line[0] == "#":
    return

asns = curr_line.rstrip().split("|")
for i in range(0, len(asns)):
    asn = int(asns[i])

# Map the current asn if the asn is not in as_2_cone yet.
if asn not in as_2_cone:
    as_2_cone[asn] = {}
    as_2_cone[asn]["asn"] = asn
    as_2_cone[asn]["cone"] = [asn]
    as_2_cone[asn]["size"] = 1

    # Compare asns[i] to each asn that comes after it.
    for j in range(i + 1, len(asns)):
        # Call helper function to format key to have asn's sorted by value.
        key = format_key(asn, int(asns[j]))

        # Add asns with a "provider" relationship between: asn[i] asn[j]
        if key in as_pair_2_rel and as_pair_2_rel[key] == 1:
            as_2_cone[asn]["size"] += 1
            as_2_cone[asn]["cone"].append(int(asns[j]))
        else:
            break  
~~~
