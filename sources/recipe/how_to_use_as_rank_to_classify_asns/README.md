 How to use AS Rank to classify asns

~~~json
{
    "id" : "how_to_use_as_rank_to_classify_asns",
    "visibility" : "public",
    "name" : "How to use AS Rank to classify asns",
    "description" : "Using the AS Rank API, classify asns into three catagories: tansit free, middle, edge",
    "links": [{"to":"dataset:as_relationships"},{"to":"dataset:asrank"}],
    "tags" : [
        "ASN",
        "as rank",
        "as relationship",
        "IPv4"
    ],
    "authors":[
        {
            "person": "person:wolfson__donald",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## Introduction

This solution helps classify an asn based upon relationship with other asns. The following [script](api_2_class.py) takes in a list of asns the user wants to classify, and calls the ASRank API to gather AS Relationships of the asns. This is done by getting an asns total number of providers and customers, storing them in a dictionary labeled, ```as_2_data```. This data is then used to determine classifications, which are stored in a dictionary labeled ```as_2_class```. The script then prints to STDOUT the classification of requested asns.

### Usage

Below is an example of how to run the script to classify the asns 3356 and 10, sending their classifications to a .jsonl file. You must use the -a flag, and provide at least on asn to classify. For classifying multiple asns, provide a comma seperated list with no spaces.
- Note: This script calls the API until all AS Relationships are found, and this can take a significant amount of time.

```bash
python3 api_2_class.py -a 3356,10 > output.jsonl
```

## Solution

Below is are two helper methods used to get a query from the ASRank API, and parse it. The first method shows all the data that is taken from ASRank, with the most important being in the "node" segment. This segment is then given to the second helper method which updates a dictionary named ```as_2_data``` tracking an asn's provider and customers.

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
def update_as_2_data(curr_line):
    global as_2_data
    global asns

    # Get the values from the current line.
    relationship = curr_line["relationship"]
    asn0 = curr_line["asn0"]["asn"]
    asn1 = curr_line["asn1"]["asn"]

    # Edge Case: Skip this line if asn0 and ans1 are not in asns.
    if asn0 not in asns and asn1 not in asns:
        return

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
    
    # If asn0's provider is asn1 increase asn0's customers, and asn1's providers
    if relationship is "provider":
        as_2_data[asn0]["providers"].add(asn1)
        as_2_data[asn1]["customers"].add(asn0)
    # Else if asn0's customer is asn1.
    elif relationship is "customer":
        as_2_data[asn0]["customers"].add(asn0)
        as_2_data[asn1]["providers"].add(asn1)
~~~

Below is a helper method used to iterate over ```as_2_data``` to update ```as_2_class``` by determining what classification to use.

~~~Python
# Helper method use to update as_2_class with data from as_2_data.
def update_classifications():
    global as_2_class
    global as_2_data

    # Iterate over each asn in as_2_data.
    for asn in as_2_data:
        # Edge Case: Create a dictionary for the asn if it doesn't exist.
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

## Background

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

### What is the ASRank API?

- ASRank is CAIDA's ranking of Autonomous Systems and organizations.
- This API uses GraphQL for API requests which can be seen in the ```as_links_query(first, offset)``` method.
- For more information on ASRank, click [here](https://asrank.caida.org/).
- For more information on ASRank's API, click [here](https://api.asrank.caida.org/v2/docs).

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
