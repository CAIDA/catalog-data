~~~json
{
    "id" : "how_to_download_from_asrank",
    "name": "How to download from AS Rank GraphQL",
    "description":"Example scripts for downloading from AS Rank's GraphQL server.",
    "links": [
        {
            "to": "dataset:asrank_api"
        }
    ],
    "tags": [
        "topology",
        "software/tools",
        "ASN",
        "geolocation"
    ],
    "authors":[
        {
            "person": "person:huffaker__bradley",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## Introduction

Introduction
AS Rankv2.1 is a GraphQL API interface. GraphQL allows clients to create queries that specify which values they require and contain multiple resources. GraphQL, as a strongly-typed language, allows to know what data is available, in what format and verify responses.

The User Interface (UI) can be found at [http://asrank.caida.org](http://asrank.caida.org). 
The Application Programming Interface version 2 (APIv2) interface is 
available at [https://api.asrank.caida.org/v2/graphql](https://api.asrank.caida.org/v2/graphql) and GraphiQL, 
graphic interface, can be found at [https://api.asrank.caida.org/v2/graphiql](https://api.asrank.caida.org/v2/graphiql).

We will be operating AS Rank APIv1 ([(http://as-rank.caida.org/api/v1](http://as-rank.caida.org/api/v1)) 
until March 1st, 2020, but it will no longer be updated. Current users 
should migrate to the v2 API before this date. Contact 
asrank-info@caida.org for migration assistance.

This solution parses through ITDK datasets and stores a node's `node id`, `isp`, `asn` and `location` as a json object. 

Sample scripts 

GraphQL works with the standard set of HTTP tools (see 4 simple ways to call a GraphQL API).

[asrank-download-asn.py](asrank-download-asn.py) is a simple Python script that can be used to 
download a single ASN. It can also be used as a template to write your own script.
~~~
python3 asrank-download-asn.py 701
~~~

[asrank-download-asnLinks.py](asrank-download-asnLinks.py) is a simple Python script that can be used to 
download a ASN links. It can also be used as a template to write your own script.
~~~
python3 asrank-download-asnLink.py 701 8245 > links.jsonl
~~~

[asrank-download.py](asrank-download.py) is a more complex Python script that can be 
used as-is to download all the ASNs, organizations, or ASN links. The following 
arguments will cause the script to download all the asns, organizations, and 
asnLinks into their respective files.
~~~
python3 asrank-download.py -v -a asns.jsonl -o organizations.jsonl -l asnLinks.jsonl -u https://api.asrank.caida.org/v2/graphql
~~~

curl The following command will download ASN 701's organization name and the number of ASNs in its cone.
~~~
curl -H "Content-Type: application/json" -X POST \
  --data '{ "query": "{ asn(asn:\"701\"){ asn organization { orgName } cone { numberAsns } } }" }' \
  https://api.asrank.caida.org/v2/graphql
~~~
