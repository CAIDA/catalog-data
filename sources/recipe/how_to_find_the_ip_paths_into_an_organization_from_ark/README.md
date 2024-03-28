~~~json
{
  "id": "how_to_find_the_ip_paths_into_an_organization_from_ark",
  "name": "How to find the IP paths into an organization from Ark?",
  "description": "This will provide a recipe to find a company's prefixes and the IP paths from CAIDA's ark to those prefixes.",
  "links": [
    {
      "to": "dataset:bgptools"
    },
    {
      "to": "software:fantail"
    },
    {
      "to": "recipe:how_to_parse_ark_traces"
    }
  ],
  "tags": [
    "measurement methodology",
    "topology",
    "software/tools",
    "ipv4",
    "ipv4 prefix"
  ],
  "authors":[
        {
            "person": "person:huffaker_bradley",
            "organizations": [ "CAIDA, San Diego Supercomputer Center, University of California San Diego" ]
        }
    ]
}
~~~
### Introduction
We will be using BGPTools to identify the set of prefixes that are announced by the organization, and 
Fantail to collect the Ark traces to the those prefixes.

### Collect Prefixes  (bgptools)
- Go to **bgp.tools** and type the organization name into the "Start here..." field. 
  <div style="margin-left:2em">
    <img width="400" src="images/start-here.png"/>
  </div>

- Choose the best **AS number** on in the "Item" column for your organization.
  <div style="margin-left:2em">
    <img width="400" src="images/select-asn.png"/>
  </div>

- Download **https://bgp.tools/table.txt** and get all the prefixes for **AS number**. 

  ~~~
  wget https://bgp.tools/table.txt
  grep ' 7377$' table-14-03-24.txt | grep -v ':' | cut -f 1 -d ' ' - | tr '\n' ',' | sed 's/.\{1\}$//' > prefixes.txt 
  ~~~ 

### Collect Traces (fantail) 
- Log into **fantail.caida.org** and select **Query traceroute paths**
  <div style="margin-left:2em">
    <img width="400" src="images/query-traceroute-paths.png"/>
  </div>

- Inside the **Query** box, set **Method** to **[ ] dest** and copy/paste the prefixes from **prefixes.txt** file into the **Target Address/Prefix** field. 

  <div style="margin-left:2em">
    <img width="400" src="images/dests.png"/>
  </div>

- Wait for the **Query Results** page to come up.

- Download **JSONL results**
  This will download the trace in a JSONL file with a single trace per line as a complete JSON object. 
  <div style="margin-left:2em">
    <img width="400" src="images/download-json.png"/>
  </div>

### Processing Traces 

- You can process each individual line with the following code snippet: 
    ~~~
    #!  /usr/bin/env python3 
    import sys
    import json 
    
    with open(sys.argv[1]) as fin: 
        for line in fin:
            trace = json.loads(line)
            print (json.dumps(info, indent=4))
    ~~~

For full details on scamper traces reference 
<a href="https://catalog.caida.org/recipe/how_to_parse_ark_traces">How
to parse through an ark traceroute?</a> recipe.

