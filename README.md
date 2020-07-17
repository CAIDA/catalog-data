## Catalog Data
This contains the source JSON files used to build the catalog's databases.
The source JSON files are found in the source directory.  These are combined 
to build id_id_link.json, id_object.json, and word_score_id.json. 


## Build the compiled data
If you have updated the source files.  You will need to recompile the catalog json files, commit
the updated data files, and then push to the server.  If you want to make it public, you will need
to merge those files into v1. 
~~~
python3 scripts/data-build.py
git commit -a 
git push
~~~

### Possible Solutions:
- Introduction to PANDA
- Introductino to Internet Data

### Possible questions:
- What is the current packet size distribution? 
- How many IP addresses are allocated to Africa? 
- How do I download a json representing the values in asran.caida.org/asns?
- How do I get a full rib file from BGPSteam?
- How many ASs do not block spoofed source addresses?
- How do I get an AS's name?
- How do I get a list of prefixes belong to a given IXP?
- Is list of ASes (A,B,C,D>..) directly connected on today's BGP tables, and since when have they been?
- What is a MOAS and how should you resolve them?
