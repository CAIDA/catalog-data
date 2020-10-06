### Catalog Data
This repo contains the source JSON files used to build the CAIDA resource catalog ([ catalog.caida.org](https://catalog.caida.org)'s database.

### wiki links
- [overview of the JSON files](https://github.com/CAIDA/catalog-data/wiki/overview).
- [how to write a recipe](https://github.com/CAIDA/catalog-data/wiki/how-to-make-a-recipe)
- [how to write a paper](https://github.com/CAIDA/catalog-data/wiki/how-to-make-a-paper)

### code 
- [[scripts/data-build.py]] compiled to generate the database files
    - id_object.json : id to object data
    - id_id_link.json : neighbors list of an id's labeled neighbors
    - word_score_id.json : dictionary 
- [[scripts/pubdb_placeholder.py]] : converts the pubdb dumps to the catalog JSON format
- [[scripts/pubdb_links.py]]: updates the links from pubdb dumps

## 
Generate the database json files by typing ```make``` on the command line.  

~~~
make
~~~

You can also do ```make clean``` to remove the pubdb files and id_\* files. 


