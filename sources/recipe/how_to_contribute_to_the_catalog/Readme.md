~~~json
{
    "id" : "how_to_contribute_to_the_catalog",
    "name": "How to contribute to the catalog",
    "description":"Overview of the process used to contribute to CAIDA's catalog.",
    "links": [ 
        "software:catalog" 
    ],
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


### Search Query

Thank you for considering contributing to CAIDA's catalog. The current version of 
the catalog's data is built from a set of JSON files which are stored in [github](https://github.com/CAIDA/catalog-data).  

    [CAIDA/catalog-data](https://github.com/CAIDA/catalog-data)

Contributions and updates are welcome from all comers. We are interested in expanding the
catalog to include non-CAIDA resources. The general process is to fork, update, check, and pull.

Overview of the process:
1. Fork the current catalog-data repo found [here](https://github.com/CAIDA/catalog-data)
2. Update/add JSON files related to your contribution.
3. Check with ```make``` that your JSON is valid and doesn't contain unknown ids.
4. Pull against the CAIDA's copy of the repo.

Let us know if you have any questions <a href="mailto:catalog-info@caida.org">catalog-info@caida.org</a>.
