# How to find the business relationships between asns

~~~json
{
    "id" : "how_to_find_the_business_relationship_between_asns",
    "visibility" : "public",
    "name" : "How to find the business relationship between asns",
    "description" : "Using .as-rel file, or API to map a pair of given asns to their relationship.",
    "links": [{"to":"dataset:as_relationships"}, {"to":"dataset:as_rank"}],
    "tags" : [
        "ASN",
        "as relationship",
        "as rank",
        "IPv4"
    ]   
}
~~~

## **<ins>Introduction</ins>**

The following solution has two scripts. One that handles a [local input](pair_2_rel.py), and one that takes no input, but [uses AS Rank's API](api_2_rel.py). Both produce a dictionary, pair_2_rel which maps a pair of given asns to their relationship.The local file script only has one flag: -r which takes in s .as-rel file, this can be downloaded [here](http://data.caida.org/datasets/as-relationships/serial-1//). While the api script takes in no input, and just calls the api until all as relationships have been found, this script is significantly slower compared to the local file version.

## Usage

Below is an example of using the local file script to parse a .as-rel file to create a mapping between a pair of asns and their relationship. This file can take in either .txt or encoded .bz2 files.

```bash
python3 pair_2_rel.py -r 20200101.as-rel.txt
```

For the api version of the script, you'll need to import [graphqlclient](https://pypi.org/project/graphqlclient/#description). Below is how to install the package:

```bash
pip3 install graphqlclient
```

Below is an example of how to run the api script to create a mapping between as pairs and their relationships. 
- Note: This code takes a significantly longer amount of time to run compared to the local file version.

```bash
python3 api_2_rel.py
```

## **<ins>Solution</ins>**

Below is the helper method used to parse a given line of the .as-rel file in the [local file script](pair_2_rel.py). This method updates the dictionary, pair_2_rel by sorting the two asns by value prior to mapping the pair to their relationship.

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

Below are two helper methods used in the [api script](api_2_rel.py). The first helper method is the AS Rank Query, and what data is taken from the API. The second helper method shows what is done with the data taken from the API. The second method assumes the input is a dictionary of the keys and values within the "node" section of the query's format. 

~~~Python
# Helper method of the formatted query.
def as_links_query(first, offset):
    return [
        "asnLinks",
        """{
        asnLinks(first:%s, offset:%s) {
            totalCount
            pageInfo {
                first
                hasNextPage
            }
            edges {
                node {
                    relationship
                    asn0 {
                        asn
                    }
                    asn1 {
                        asn
                    }
                    numberPaths
                }
            } 
        }
    }"""  % (first, offset)
    ]

# Helper method that takes in a dict to create a pair relationship.
def update_pair_2_rel(curr_line):
    global pair_2_rel
    global rel_2_key

    # Get the values from the current line.
    relationship = rel_2_key[curr_line["relationship"]]
    asn0 = int(curr_line["asn0"]["asn"])
    asn1 = int(curr_line["asn1"]["asn"])

    # Place both related AS's in par_2_rel based on value of ASes.
    if (asn0 > asn1):
        temp = asn0
        asn0 = asn1
        asn1 = temp
        relationship = -1 * relationship

    key = str(asn0) + " " + str(asn1)

    # Add the pair's relationship if doesn't already exist.
    if key not in pair_2_rel:
        pair_2_rel[key] = relationship
~~~

This helper method is offered to show how to easily access a relationship in pair_2_rel in either script. This method also shows how to format two given asns to match the key format of pair_2_rel. The commented out return line could be helpful for testing, or to better understand what the relationship between the ases mean.

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
        # return str(asn0) + "'s " + str(rel) + " is " + str(asn1)
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
as0 as1 rel
10   2  -1     10's customer is 2 (p2c)
10   3   0     10's peer is 3 (p2p)
10   4   1     10's provider is 4 (c2p)
~~~

### What is the ASRank API?

- ASRank is CAIDA's ranking of Autonomous Systems and organizations.
- This API uses GraphQL for API requests which can be seen in the ```as_links_query(first, offset)``` method.
- For more information on ASRank, click [here](https://asrank.caida.org/).
- For more information on ASRank's API, click [here](https://api.asrank.caida.org/v2/docs).

### Caveats

A pair of asns is sorted by their values in ascending order. Ex: ```10 15```, you'll never see a key formatted as: ```15 10```. This reduces memory by ensuring two asns won't have both of their relationships in the dictionary. However this means the user has to sort the asns prior to accessing the data. This is why the helper method: ```get_relationship(ans0, asn1)``` is provided.

### File Format: .as-rel

Below is an example of the possible lines found in a .as-rel file. For the purpose of this solution and script, we will ignore all line that start with "#" since they will not be needed.

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
