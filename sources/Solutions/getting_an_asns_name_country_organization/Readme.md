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
Introduction

What is an AS? 
    • An AS can be broadly be thought of as a single organization, or a collection of routers that route groups of IP addresses under a common administration, typically a large organization or an ISP (Internet Service Provider). \
    • It is a connected group of one or more IP addresses (known as IP prefixes) that provide a common way to route internet traffic to systems outside the AS.
    • Each AS is responsible for routing traffic within itself. This is known as intra-AS routing. 
    • Each AS can also route traffic between itself and other autonomous systems. This is known as inter-AS routing. 
    • More information on AS can be found here: https://www.cs.rutgers.edu/~pxk/352/notes/autonomous_systems.html

What is an ASN?
    • Each AS is assigned a unique ASN, or Autonomous System Number that allows it to be uniquely identified during routing. 

What is an ASN's organization? 
    • Each ASN can be mapped to a organization that controls multiple AS's over its network. 

What is an ASN's country? 
    • The country where the ASN's organization is located. 

Mapping ASN's to country
One way to map a ASN to a country is by using the country of its organization. 

https://www.caida.org/data/as-organizations/

The AS Organization files contain two different types of entries: AS numbers and
organizations. The two data types are divided by lines that start with
'# format....'. An example can be found below.  The country value is stored on the organization
field.  Create a hash mapping organizations to country and use that to match from ASN to 
organization to country.

example AS Organization file
~~~
# format: org_id|changed|name|country|source
LVLT-ARIN|20120130|Level 3 Communications, Inc.|US|ARIN
# format: aut|changed|aut_name|org_id|opaque_id|source
1|20120224|LVLT-1|LVLT-ARIN|e5e3b9c13678dfc483fb1f819d70883c_ARIN|ARIN
~~~
----------
AS fields
----------
aut     : the AS number
changed : the changed date provided by its WHOIS entry
aut_name    : the name provide for the individual AS number
org_id  : maps to an organization entry
opaque_id   : opaque identifier used by RIR extended delegation format
source  : the RIR or NIR database which was contained this entry

--------------------
Organization fields
--------------------
org_id  : unique ID for the given organization
           some will be created by the WHOIS entry and others will be
           created by our scripts
changed : the changed date provided by its WHOIS entry
name    : name could be selected from the AUT entry tied to the
           organization, the AUT entry with the largest customer cone,
          listed for the organization (if there existed an stand alone
           organization), or a human maintained file.
country : some WHOIS provide as a individual field. In other cases
           we inferred it from the addresses
source  : the RIR or NIR database which was contained this entry


example script
~~~python
import re
re_format = re.compile("# format:(.+)")

orgs  = {}
asns = {}
with open(filename) as f:
    for line in f:
        m = re_format.search(line)
        if m:
            keys = m.group(1).rstrip().split(",")

        # skips over comments
        if len(line) == 0 or line[0] == "#":
            continue
        values = line.rstrip().split("|")
        info = {}
        id_ = values[0]
        for i,key in enumerate(keys):
            info[key] = values[i]
            if key == "country":
               org_country[id_] = values[i]
       
        if key[0] == "org_id":
            orgs[id_] = info
            info["asns"] = []
        else:
            orgs[info["org_id"]]["asns"].append(id_)
            asns[id_] = info
~~~
