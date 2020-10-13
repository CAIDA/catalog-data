## Catalog Data
This contains the source JSON files used to build the [CAIDA's catalog](https://catalog.caida.org/).
The source JSON files are found in the source directory.  

## How to contribute

If you would like to contribute to the catalog:
  - [how to contribute](https://github.com/CAIDA/catalog-data/wiki/how-to-contribute) to the catalog
  - [how to contribute a recipe](https://github.com/CAIDA/catalog-data/wiki/how-to-contribute-a-recipe) to the catalog

## Overview of these files

These are combined to build id_id_link.json, id_object.json, and word_score_id.json. 

There are three derived files generated from the object meta data.
- id_object.json : a id to object dictionary, it has all the object data execpt for links
- id_id_link.json : stores the link files in {from,to,label} nested dictionaries
- word_score_id.json : dictionry for each word of scores and id pairs.

These are made by two scripts:
- scripts/pubdb_placeholder.py : creates the pubdb objects
- scripts/data-build.py : creates the id_object.json, id_id_link.json, and word_score.id objects

## Build the catalog data
You will need to have b4 install in python3.  You can do this using
virtualenv.
~~~bash
virtualenv env
source env/bin/active
pip3 install bs4
~~~

Both of these scripts can be run using the [Makefile](Makefile).  Simply type ```make```.

~~~
# If you haven't activated virtualenv yet
# You need only do this once per shell
source env/bin/active 

make
~~~

You can also do ```make clean``` to remove the pubdb files and id_\* files. 
