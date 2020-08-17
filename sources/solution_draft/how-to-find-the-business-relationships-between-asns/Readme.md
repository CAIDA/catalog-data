# 

~~~json
{
    "id" : "how-to-find-the-business-relationship-between-asns",
    "visibility" : "public",
    "name" : "How to find the business relationship between asns",
    "description" : "Using .as-rel file formats to map a pair of given asns to get their relationships.",
    "links": [{"to":"dataset:as_relationships"}],
    "tags" : [
        "ASN",
        "as relationship",
        "IPv4"
    ]   
}
~~~

## **<ins>Introduction</ins>**

The following [script](pair_2_rel.py) produces a dictionary, pair_2_rel which maps a pair of given asns to their relationship. The script only has one flag: -r which takes in .as-rel files, which can be downloaded [here](https://www.caida.org/data/as-relationships/).

## Usage

Below is an example of using the script to parse a .as-rel file to creates a mapping between a pair of asns and their relationship. This file can take in either .txt or encoded .bz2 files.

```bash
python3 pair_2_rel.py -r 20200101.as-rel.txt
```

## **<ins>Solution</ins>**

Below is the helper method used to parse a given line of the .as-rel file. This method updates the dictionary, pair_2_rel by sorting the two asns by value prior to mapping the pair to their relationship.

~~~Python
# Parse a given line of the as_rel_file and map two ASes to their relationship.
def parse_as_rel_line(curr_line):
    global pair_2_rel

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    as_rel_set = curr_line.split("|")
        
    # Get each piece of data from the current line.
    asn0 = as_rel_set[0]
    asn1 = as_rel_set[1]
    relationship = int(as_rel_set[2])

    # Place both related AS's in pair_2_rel based om value of ASes.
    if (asn0 > asn1):
        temp = asn0
        asn0 = asn1
        asn1 = temp
        relationship = -1 * relationship

    key = asn0 + " " + asn1

    # Add the pair's relationship if doesn't already exist.
    if key not in pair_2_rel:
        pair_2_rel[key] = relationship
~~~

This helper method is offered to show how to easily access a relationship in pair_2_rel. This method also show how to format two given asns to match the key format of pair_2_rel. The commented out return line could be helpful for testing, and to see how the given asns were formatted if their key exists.

~~~Python
# Helper function to format two given asns into a key for as_pair_2_rel. 
def get_relationship(asn0, asn1):
    global pair_2_rel

    if (asn0 > asn1):
        temp = asn0
        asn0 = asn1
        asn1 = temp

    key = str(asn0) + " " + str(asn1)

    # Return the relationship, or return None if the key isn't valid.
    if key in pair_2_rel:
        rel = pair_2_rel[key]
        return rel
        # return "asn0: " + str(asn0) + " asn1: " + str(asn1) + " rel: " + rel
    else:
        return None
~~~

## **<ins>Background</ins>**

### What is an AS Relationship

- An AS Relationship is the determined routing policy between two ASes.
- The three most common types of AS Relationships are:
  - customer-to-provider (c2p) (or if looked at from the opposite direction,  provider-to-customer p2c),
  - peer-to-peer (p2p),
  - sibling-to-sibling (s2s)
- A p2p link connect two ISPs who have agreed to exchange traffic between each other and their customer's. This can allow growing ISPs savings on transit costs compared to c2p relationships.
- An s2s link connects two ASes with a common administrative boundary. Such links usually appear as a result of mergers and acquisitions, or under certain network management scenarios.
- More information on AS Relationships can be found [here](https://www.caida.org/data/as-relationships/)

~~~text
as0 as2 rel
 10   2  -1     10 is a provider of 2 (p2c)
 10   3   0     10 is a peer of 3 (p2p)
 10   4   1     10 is a customer of 4 (c2p)
~~~

### Caveats

A pair of asns is sorted by having the asn whose value is less than the other coming first. Ex: ```10 15```, you'll never see a key formatted as: ```15 10```. This reduces memory by ensuring two asns won't have both of their relationships in the dictionary. However this means the user has to sort the asns prior to accessing the data. This is why the helper method: ```get_relationship(ans0, asn1)``` is provided.

### File Format: .as-rel

Below is an example of the possible lines found in a .as-rel file. For the purpose of this solution and script, we will ignore all line that start with "#" since they will nont be needed.

~~~text
# source:topology|BGP|<data>|<system>|<monitor>
# step 1: set peering in clique
# step 2: initial provider assignment
# step 3: providers for stub ASes #1
# step 4: provider to larger customer
# step 5: provider-less networks
# step 6: c2p for stub-clique relationships
# step 7: fold p2p links
# step 8: everything else is p2p
<asn0>|<asn1>|<relationship>
~~~
