## Catalog Data
This contains the source JSON files used to build the catalog's databases.
The source JSON files are found in the source directory.  These are combined 
to build id_id_link.json, id_object.json, and word_score_id.json. 

There are three derived files generated from the object meta data.
- id_object.json : a id to object dictionary, it has all the object data execpt for links
- id_id_link.json : stores the link files in {from,to,label} nested dictionaries
- word_score_id.json : dictionry for each word of scores and id pairs.

These are made by two scripts:
- scripts/pubdb_placeholder.py : creates the pubdb objects
- scripts/data-build.py : creates the id_object.json, id_id_link.json, and word_score.id objects

## Build the compiled data
Both of these scripts can be run using the [Makefile](Makefile).  Simply type ```make```.

~~~
make
~~~

You can also do ```make clean``` to remove the pubdb files and id_\* files. 

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
