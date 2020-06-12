~~~json
{
    "name": "How do you found an ASN's country?",
    "description":"Using the ASN's organizatoin's country in WHOIS to map an ASN to the country of it's headquarters.",
    "links": ["dataset:AS_Organization"],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools"
    ]
}
~~~
One way to map a ASN to a country is by using the country of it's organization. 

https://www.caida.org/data/as-organizations/

The AS Organization files contain two different types of entries: AS numbers and
organizations.  The two data types are divided by lines that start with
'# format....'. An example can be found below.   The country value is stored on the organization
field.  Create a hash mapping organizations to country and use that to match from ASN to 
organization to country.

example AS Organization file
~~~
# format: org_id|changed|name|country|source
LVLT-ARIN|20120130|Level 3 Communications, Inc.|US|ARIN
# format: aut|changed|aut_name|org_id|opaque_id|source
1|20120224|LVLT-1|LVLT-ARIN|e5e3b9c13678dfc483fb1f819d70883c_ARIN|ARIN
~~~

example script
~~~python
import re
re_format = re.compile("# format:(.+)")

org_country = {}
asn_country = {}
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
        else:
            asn[id_] = info
            
  for asn,country in asn_country.items():
     print (asn,country)
~~~
