# How to use AS Relationships to classify asns

~~~json
{
    "id" : "how_to_look_up_as's_rank_using_as_relationship_file",
    "visibility" : "public",
    "name" : "How to look up AS's rank using AS Relationship file",
    "description" : "Using a given AS Relationship, classify all asns into three catagories: tansit free, middle, edge",
    "links": [{"to":"dataset:as_relationships"}],
    "tags" : [
        "ASN",
        "as relationship",
        "IPv4"
    ]
}
~~~

## **<ins>Introduction</ins>**

This solution helps classify an asn based upon its relationships to other asns. The following [script](rel_2_class.py) takes in all AS Relationships from a local .as-rel file to determine every asn's classification. This is done by getting the number of providers and customers of each asn, storing them in a dictionary labeled, ```as_2_data```. This data is then used to determine classifications, which are stored in a dictionary labeled ```as_2_class```. The classifications for each asn is then printed to STDOUT.

### Usage

Below is an example of how to run the script on AS Relationships dataset from Jan 1st, 2020, sending the classifications to a .jsonl file. You must use the -r flag, and provide a path to a local .as-rel file. AS Relationship datasets can be downloaded [here](https://www.caida.org/data/as-relationships/).
- Note: This script can take in both .txt and encoded .bz2 files, so you don't have to decode the downloaded datasets.

```bash
python3 api_2_class.py -r 20200101.as-rel.txt > output.jsonl
```

## **<ins>Solution</ins>**

Below is a helper method used to parse a given line from a .as-rel file. This is called once opening the given file and iterating over each line. The line is split into it's three values, which are then used to update ```as_2_data``` with each asn's providers and customers.

~~~Python
# Helper method that takes in a line from the .as-rel file to update as_2_data.
def parse_as_rel_line(curr_line):
    global as_2_data
    global rel_2_name

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    # curr_line format: <asn0>|<asn1>|<relationship>
    asn0, asn1, relationship = curr_line.split("|")

    # Edge Case: Create objects for asn0 or asn1 if they are not in as_2_data.
    if asn0 not in as_2_data:
        as_2_data[asn0] = {
            "providers" : set(),
            "customers" : set()
        }
    if asn1 not in as_2_data:
        as_2_data[asn1] = {
            "providers" : set(),
            "customers" : set()
        }
    
    # If asn0's provider is asn1 add to asn0's customers, and asn1's providers.
    if rel_2_name[int(relationship)] == "provider":
        as_2_data[asn0]["providers"].add(asn1)
        as_2_data[asn1]["customers"].add(asn0)
    # Else if asn0's customer is asn1.
    elif rel_2_name[int(relationship)] == "customer":
        as_2_data[asn0]["customers"].add(asn1)
        as_2_data[asn1]["providers"].add(asn0)
~~~

Below is a helper method used to iterate over ```as_2_data``` to update ```as_2_class``` by determining what classification to used based on a given asn's providers and customers.

~~~Python
# Helper method use to update as_2_class with data from as_2_data.
def update_classifications():
    global as_2_class
    global as_2_data

    # Iterate over each asn in as_2_data.
    for asn in as_2_data:
        # Edge Case: Create a dictionary for the asn if it doesnn't exist.
        if asn not in as_2_class:
            as_2_class[asn] = {
                "asn" : asn,
                "class" : None
            }
        # If asn has no providers, then it is transit free.
        if len(as_2_data[asn]["providers"]) == 0:
            as_2_class[asn]["class"] = "transit free" 
        # Else if asn has no customers. then it is an edge.
        elif len(as_2_data[asn]["customers"]) == 0:
            as_2_class[asn]["class"] = "edge"
        # Else asn has some providers and customers, then it is a middle.
        else:
            as_2_class[asn]["class"] = "middle"
~~~

## **<ins>Background</ins>**

### What is an AS Relationship?
- An AS Relationship is the determined routing policy between two ASes.
- The three most common types of AS Relationships are:
  - customer-to-provider (c2p) (or if looked at from the opposite direction,  provider-to-customer p2c),
  - peer-to-peer (p2p),
  - sibling-to-sibling (s2s)
- A p2p link connect two ISPs who have agreed to exchange traffic between each other and their customer's. This can allow growing ISPs savings on transit costs compared to c2p relationships.
- An s2s link connects two ASes with a common administrative boundary. Such links usually appear as a result of mergers and acquisitions, or under certain network management scenarios.
- More information on AS Relationships can be found [here](https://www.caida.org/data/as-relationships/)

~~~text
as0 as1 rel
10   2  -1     10's customer is 2 (p2c)
10   3   0     10's peer is 3 (p2p)
10   4   1     10's provider is 4 (c2p)
~~~

### Data Structure Format: as_2_data

~~~Python
{
    "asn0" : {
        "providers" : set(),        # Set of asns that are providers to asn0.
        "customers" : set()         # Set of asns that are customers to asn0.
    }
}
~~~

### Data Structure Format: as_2_class

~~~Python
{
    # asn0 has zero providers.
    "asn0" : { "asn":"asn0", "class":"transit free" },
    # asn1 has both providers and customers.
    "asn1" : { "asn":"asn1", "class":"middle" },
    # asn2 has zero customers.
    "asn2" : { "asn":"asn2", "class":"edge" }
}
~~~

### Data Structure Format: rel_2_name

~~~Python
rel_2_name = {
    -1 : "customer",
    0: "peer",
    1: "provider"
}
~~~
