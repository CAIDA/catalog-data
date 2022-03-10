~~~json
{
    "id" : "how_to_contribute_to_the_catalog",
    "name": "How to contribute to the catalog",
    "description":"Overview of the process used to contribute to CAIDA's catalog.",
    "links": [ 
        "software:catalog" 
    ],
    "tags": [
        "contribute",
        "catalog help"
    ],
    "authors":[
        {
            "person": "person:huffaker__bradley",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ],
    "resources": [
        {
            "name":"how to contribute",
            "url":"https://github.com/CAIDA/catalog-data/wiki/how-to-contribute"
        },
        {
            "name":"contribute a recipe",
            "url":"https://github.com/CAIDA/catalog-data/wiki/how-to-contribute-a-recipe"
        }
    ]
}
~~~


### Search Query

Thank you for considering contributing to CAIDA's catalog. The current version of 
the catalog's data is built from a set of JSON files which are stored in [https://github.com/CAIDA/catalog-data](https://github.com/CAIDA/catalog-data).
   

Contributions and updates are welcome from all comers. We are interested in expanding the
catalog to include non-CAIDA resources. The general process is to fork, update, check, and pull.

### overview of process:

   1. fork the current catalog-data repo
  
   1. update/add JSON files related to your contribution
  
   1. check with ```make``` that your JSON is valid and doesn't contain unknown ids
  
   1. pull against the CAIDA's copy of the repo.

Let us know if you have any questions <a href="mailto:catalog-info@caida.org">catalog-info@caida.org</a>.
