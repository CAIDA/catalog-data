~~~json
{
    "name": "How to get an ASN's name, country and organization?",
    "description":"Using the ASN's organizatoin's country in WHOIS to map an ASN to the country of it's headquarters.",
    "links": ["dataset:AS_Organization"],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools",
        "ASN",
        "geolocation"
    ]
}
~~~
### Introduction ###

**What is an AS?**\
 • An AS can be broadly be thought of as a single organization, or a collection of routers that route groups of IP addresses under a common administration, typically a large organization or an ISP (Internet Service Provider). \
 • It is a connected group of one or more IP addresses (known as IP prefixes) that provide a common way to route internet traffic to systems outside the AS.\
 • Each AS is responsible for routing traffic within itself. This is known as intra-AS routing. \
 • Each AS can also route traffic between itself and other autonomous systems. This is known as inter-AS routing. \
 • More information on AS can be found here: https://www.cs.rutgers.edu/~pxk/352/notes/autonomous_systems.html 

**What is an ASN?**\
    • Each AS is assigned a unique ASN, or *Autonomous System Number* that allows it to be uniquely identified during routing.

**What is an ASN's organization?**\
    • Each ASN can be mapped to a organization that controls multiple AS's over its network. 

**What is an ASN's country?** \
    • The country where the ASN's organization is located. 

### Mapping ASN's to country ###
*Datasets can be found here* : https://www.caida.org/data/as-organizations/

One way to map a ASN to a country is by using the **country of its organization.** 

The AS Organization files contain two different types of entries: AS numbers and
organizations.\
The two data types are divided by lines that start with
'# format....'.  \ 
An example can be found below. \
The country value is stored on the organization
field.\
Create a hash mapping organizations to country and use that to match from ASN to 
organization to country.

Example of the AS organization in a test file:
~~~
# format: org_id|changed|name|country|source
LVLT-ARIN|20120130|Level 3 Communications, Inc.|US|ARIN
# format: aut|changed|aut_name|org_id|opaque_id|source
1|20120224|LVLT-1|LVLT-ARIN|e5e3b9c13678dfc483fb1f819d70883c_ARIN|ARIN
~~~

### Explanation of the data fields ###

--------------------
Organization fields
--------------------
 org_id  : unique ID for the given organization, \
 changed : the changed date provided by its WHOIS entry \
 name    : name could be selected from the AUT entry tied to the
           organization, the AUT entry with the largest customer cone,
          listed for the organization (if there existed an stand alone
           organization), or a human maintained file. \
 country : some WHOIS provide as a individual field. In other cases
           we infer it from the addresses \
 source  : the RIR or NIR database which contained this entry 

----------
AS fields
----------
aut     : the AS number \
changed : the changed date provided by its WHOIS entry \
aut_name : the name provide for the individual AS number \
org_id  : maps to an organization entry \
opaque_id   : opaque identifier used by RIR extended delegation format \
source  : the RIR or NIR database which was contained this entry 

example script
~~~python
import re

filename = 'tester'
re_format= re.compile("# format:(.+)")


asn_names = {}
org_country = {}
org_asns = {}
org_id_name = {}


with open(filename) as f:
    for line in f:
        m = re_format.search(line)
        if m:
            keys = m.group(1).rstrip().split(",")
           
        # skips over comments
        if len(line) == 0 or line[0] == "#":
            continue

        values = line.rstrip().split("|")
    
        #Dictionary that holds the ASN id mapping 
        info = {}

        #id - org_id and ASN
        id_ = values[0]
    
        

        for i, key in enumerate(keys):
            
            if "org_name" in key:
                # Map org_id to country
                org_country[id_] = values[3]
                # Map org_id to org_name
                org_id_name[id_] = values[2]
                
            
            if 'aut' in key:
                # Map asn to org_id
                org_asns[id_] = values[3]
        
                # Map asn to asn_name
                asn_names[id_] = values[2]
                info = org_asns

    # Convert values to a list        
    info = {k: v.split() for k, v in info.items()}

    # Iterate through asn:org_id 
    for asn, org_id in org_asns.items():
        # Insert asn_name at the front of list
        if asn in asn_names:
            info[asn].insert(0, asn_names[asn]) 
        # Append org_name
        if org_id in org_id_name:
            info[asn].append(org_id_name[org_id])
        # Append country
        if org_id in org_country:
            info[asn].append(org_country[org_id])
          
    print(info)
~~~
