### Catalog Data
This repo contains the source JSON files used to build the CAIDA resource catalog ([ catalog.caida.org](https://catalog.caida.org))'s database.

The Makefile supports the following commands:
- *run* (default): this will build the data files with up-to-date dates and un-indented output
- *fast* : this will build the data files without up-to-date dates and un-indented output
- *read*,*readable* : this will build the data files without up-to-date dates and indented output
  this version is more human readable output
- *clean* : this will remove all the placeholder files

### how to links
- [how to contribute to the catalog](https://github.com/CAIDA/catalog-data/wiki/how-to-contribute)
     - [how to contribute a recipe](https://github.com/CAIDA/catalog-data/wiki/how-to-contribute-a-recipe)
- [data-papers.yaml format](https://wiki.caida.org/twiki/bin/view/CAIDA/ExternalDataPaperEntry)


### code 
- [scripts/data-build.py](scripts/data-build.py) compiled to generate the database files
    - id_object.json : id to object data
    - id_id_link.json : neighbors list of an id's labeled neighbors
    - word_score_id.json : dictionary 
- [scripts/pubdb_placeholder.py](scripts/pubdb_placeholder.py) : converts the pubdb dumps to the catalog JSON format
- [scripts/pubdb_links.py](scripts/pubdb_links.py): updates the links from pubdb dumps

## 
Generate the database json files by typing ```make``` on the command line.  
If you would like to contribute to the catalog:
  - [how to contribute](https://github.com/CAIDA/catalog-data/wiki/how-to-contribute) to the catalog
  - [how to contribute a recipe](https://github.com/CAIDA/catalog-data/wiki/how-to-contribute-a-recipe) to the catalog

## Overview of these files

The catalog is built from three sources: CAIDA's pubdb database, local json files in sources dirctory,
and markdown files stored in the catalog-data-caida repository.  The  pubdb is a seperate database and we 
    parse a static dump here [PANDA-Papers-json.pl.json](data/PANDA-Papers-json.pl.json) and [PANDA-Presentations-json.pl.json](data/PANDA-Presentations-json.pl.json).
The raw caida metadata files are kept in catalog-data-caida to allow a different set of permissions. 

The original and convert JSON files are parsed by [data-build.py](scripts/data-build.py) are then used to generate: 
- id_object.json : a id to object dictionary, it has all the object data execpt for links
- id_id_link.json : stores the link files in {from,to,label} nested dictionaries
- word_score_id.json : dictionary for each word of scores and id pairs.
- types_ids.json : mapps the object types and the ids of that type 
- suggestions.json : a list of suggestions for 0 results queries copied from data/suggestions.json
  The order of suggestions in the file, is the 'default order'

These are made by two scripts:
- scripts/pubdb_placeholder.py : creates the pubdb objects
- scripts/data-build.py : creates the id_object.json, id_id_link.json, and word_score.id objects

## Build the catalog data

### 1. Start your Environment
#### Windows
If you are on a Windows system, you will need to install a Linux terminal for Windows.
- https://ubuntu.com/tutorials/ubuntu-on-windows#1-overview

Then run the following commands:
~~~
sudo apt install make 
sudo apt install python3-pip
pip3 install -r requirements.txt 
python3 -m nltk.downloader all
~~~

#### Unix/Mac
You will need to have b4 installed in python3.  You can do this using
virtualenv.
~~~bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
~~~
##### download NLTK
https://www.nltk.org/data.html (own-1.4)

### 2. Get catalog-data-caida (if you have access, else skip to 3)
All the CAIDA datasets are stored in catalog-data-caida, which has restricted access.
If you have access to this repo you should clone it, if not then its IDs will be 
supplied by data/data_id___caida.json.

a. Make a new clone
~~~
## clone the repo if you do not have it (inside of catalog-data, as a sub directory)
clone git@github.com:CAIDA/catalog-data-caida.git
~~~

b. **Or** if you already have the catalog-data-caida repo cloned, update the catalog-data-caida 
~~~bash
cd catalog-data-caida
git checkout v1
git pull
~~~

### 3. Run make
This will be handled by the [Makefile](Makefile).
~~~bash
make
~~~


~~~bash
# If you haven't activated virtualenv yet
# You need only do this once per shell
source env/bin/activate 

make
~~~

You can also do ```make clean``` to remove the pubdb files and id_\* files. 

## Notes on catalog-data-caida usage
If you do have access to catalog-data-caida and may often update both repos, try making a symlink between your catalog-data and catalog-data-caida repositories so that you only keep 1 copy of each repository. For example, your directory structure may look like this:
~~~
catalog-data
 |-> catalog-data-caida -> ../catalog-data-caida
catalog-data-caida
~~~
