~~~json
{
    "id" : "how_to_contribute_to_the_catalog",
    "name": "How to contribute to the catalog",
    "description":"Overview of the process used to contribute to CAIDA's catalog.",
    "links": [ "software:catalog" ],
    "tags": [
        "contibute",
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
            "name":"contribute general",
            "url":"https://github.com/CAIDA/catalog-data/wiki/how-to-contribute"
        },
        {
            "name":"contribute recipe",
            "url":"https://github.com/CAIDA/catalog-data/wiki/how-to-contribute-a-recipe"
        }
    ]
}
~~~


### search query

Thank you for considering contributing to CAIDA's catalog. The current version of 
the catalog's data is built from a set of JSON files which are stored in github.  

    [CAIDA/catalog-data](https://github.com/CAIDA/catalog-data)

Contributions and updates are welcome from all comers.  We are interested in expanding the
catalog to include non CAIDA resources. The general process is to fork, update, check, and pull.

overview of process:
1. fork the current catalog-data repo
1. update/add JSON files related to your contribution
1. check with ```make``` tha your JSON is valid and doesn't contain unknown ids
1. pull against the CAIDA's copy of the repo.

Let us know if you have any questions <a href="mailto:catalog-info@caida.org">catalog-info@caida.org</a>.
