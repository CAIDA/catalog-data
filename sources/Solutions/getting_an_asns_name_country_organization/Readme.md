~~~json
{
    "id":"solution:getting_an_asns_name_country_organization",
    "visibility": "public",
    "name": "How to get an ASN's name, organization and country?",
    "description":"Using the ASN's organization's country in WHOIS to map an ASN to the country of it's headquarters.",
    "links": [{"to":"dataset:AS_Organization"}],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools",
        "ASN",
        "geolocation",
        "organization",
        "country"
    ]
}
~~~

### <ins> Introduction </ins> ###

### <ins> Mapping ASN's to country </ins> ###
*AS to Organization Mapping Datasets:* [link](https://www.caida.org/data/as-organizations/)

One way to map a ASN to a country is by mapping to the **country of its organization.** 

The AS Organization files contain two different types of entries: AS numbers and
organizations.\
The two data types are divided by lines that start with
'# format....'.\
An example can be found below.\
Note: The `country` field is stored on the organization field format. 

Example of the AS organization in a test file:
~~~
# format: org_id|changed|org_name|country|source
LVLT-ARIN|20120130|Level 3 Communications, Inc.|US|ARIN
# format: aut|changed|aut_name|org_id|opaque_id|source
1|20120224|LVLT-1|LVLT-ARIN|e5e3b9c13678dfc483fb1f819d70883c_ARIN|ARIN
~~~

### Explanation of the data fields ###

--------------------
Organization fields
--------------------

 **org_id** : unique ID for the given organization \
 **changed** : the changed date provided by its WHOIS entry \
 **name**    : the name of the organization. The name could be selected from the AUT entry tied to the
               organization, the AUT entry with the largest customer cone,
               listed for the organization (if there existed an stand alone
               organization), or a human maintained file. \
 **country** : The country where the organization is located. Some WHOIS provide this field as a individual field. In other                cases we infer it from the addresses \
 **source**  : the RIR or NIR database which contained this entry 

----------
AS fields
----------
**aut**     : the AS number or asn \
**changed** : the changed date provided by its WHOIS entry \
**aut_name** : the name provided for the individual AS number \
**org_id**  : maps to an organization entry \
**opaque_id**   : opaque identifier used by RIR extended delegation format \
**source**  : the RIR or NIR database which was contained this entry 

    
### <ins> Solution </ins> ###
The following script returns a dictionary `asn_info` that maps an ASN id to other field values `asn`, `changed`, `asn_name`, `org_id`, `source`, `org_name` and `country` in the following format:\
{'12285': {`asn`: '12285', `changed`: ' ', `asn_name`: ' ', 
`org_id`: ' ', `source`: '', `org_name`: ' ', `country`: ' ' }

 ~~~python
import re
import sys

re_format= re.compile("# format:(.+)")

org_info = {}
asn_info = {}

# Pass in test dataset as filename
with open(filename) as f:
    for line in f:
        m = re_format.search(line)
        if m:
            keys = m.group(1).rstrip().split(",")
            keys = keys[0].split("|")
            if keys[0] == 'aut':
                # Replace all instances of 'aut' with 'asn'
                keys[0] = 'asn'
                # Replace all instances of 'aut_name' with 'asn_name'
                keys[2] = 'asn_name'

            
        # skips over comments
        if len(line) == 0 or line[0] == "#":
            continue

        values = line.rstrip().split("|")
    
        info = {}

        for i,key in enumerate(keys):
            info[keys[i]] = values[i]
           

        if "asn" == keys[0]:
            org_id = info["org_id"]
            if org_id in org_info:
                for key in ["org_name","country"]:
                    info[key] = org_info[org_id][key]
             
            asn_info[values[0]] = info

        elif "org_id" == keys[0]:
            org_info[values[0]] = info
        else:
            print ("unknown type",keys[0],file= sys.stderr)

# Contains the asn mapping to other field values in this format:
# {'12285': {'asn': '12285', 'changed': '20011231', 'asn_name': 'ONE-ELEVEN', 
# 'org_id': '111S-ARIN', 'source': 'ARIN', 'org_name': 'One Eleven Internet Services', 'country': 'US' }
# print(asn_info)       
            
~~~
### <ins> Background </ins> ###

**What is an AS?**\
 • AS stands for Autonomous system.\
 • It can be broadly be thought of as a single organization, or a collection of routers that route groups of IP addresses under a common administration, typically a large organization or an ISP (Internet Service Provider). \
 • It is a connected group of one or more IP addresses (known as IP prefixes) that provide a common way to route internet traffic to systems outside the AS.\
 • Each AS is responsible for routing traffic within itself. This is known as intra-AS routing. \
 • Each AS can also route traffic between itself and other autonomous systems. This is known as inter-AS routing. \
 • More information on AS can be found [here]( https://www.cs.rutgers.edu/~pxk/352/notes/autonomous_systems.html) and [here](https://www.caida.org/publications/presentations/2016/as_intro_topology_wind/as_intro_topology_wind.pdf)

**What is an ASN?**\
    • Each AS is assigned a unique ASN, or *Autonomous System Number* that allows it to be uniquely identified during routing.

**What is an ASN's organization?**\
    • Each ASN can be mapped to a organization that controls multiple AS's over its network. 

**What is an ASN's country?** \
    • The country where the ASN's organization is located. 
    
### <ins> Caveats </ins> ###

For Multi-National Corporations, or MNCs, (where multiple ASNs for the same organization are located in the same country or close neighboring countries) this ASN to country mapping would be an **oversimplification**, as the `country` would represent the ASN's headquarters but not the physical infrastructure. 
In other words, the MNC ASN's will map back to the country where the headquarters are located, but not countries where all possible physical infrastucture is located. 

