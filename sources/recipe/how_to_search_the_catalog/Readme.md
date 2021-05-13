~~~json
{
    "id" : "how_to_search_the_catalog",
    "name": "How to search the catalog",
    "description":"Overview of the more advanced catalog search features.",
    "links": [ "software:catalog" ],
    "tags": [
        "search",
        "catalog help",
        "catalog"
    ],
    "authors":[
        {
            "person": "person:huffaker__bradley",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~


### Search Query

One of the primary ways people can interact with the catalog is with a search query. A search query is a search against the catalog for objects linked against a set of object ids, matching a set of types, and/or containing a set of words. A search query is a case insentive unordered collection of object ids, key/value pairs, and words.

A search query can be generated from a search string by splitting the string on white space into tokens and dividing the tokens into ids, key/value pairs, and words.
<style>
    table {
        border-style: solid;
    }
</style>

| type | meaning | examples |
|------|------------|---------|
| **key/value** ``(key)=(value)`` | a key and a value pair  | types=dataset,recipe | 
| **id** , -**id**      ``(type):(shortName)``  | an object id | dataset:as_rank_online , -tag:asn | 
| **word** , -**word**     | anything that doesn't match the above | rank , -topology |

- **words** (rank)

   An object is added to the matching set if it contains all the supplied words in a text field (''name'', ''organization'', etc) or 
   a child's text field ("paper's author's organization"). If no words are provided, all objects are added to the matching set.

    - **-word** (-rank)

       A **-** in front of the word, reverse it's meaning and removes objects from the matching set if the word is found in a field.

- **key=value(s) pairs** (types=paper,dataset)

   Each key/value pair has a single key, which defines the type of value, and a comma seperated list of values. The list of values is processed as a "or" operator,
   i.e. an object is returned if it matches any of the values. 

     |   key    |    value     | 
     |----------|--------------|
     |   types  |  comma separated list of object types <br>  `types=dataset`  &nbsp;&nbsp;&nbsp;  `types=media,recipe`  | 
     |   persons | comma separated list of strings matching part of a person's names<br> `persons=john` will returns all persons with john in thier name  |  
     |   ids     | comma seperated list of object ids <br> `ids=paper:2021_wie2020_report,media:2020_lvee_online_edition_ithena`  |
      
- **ids** (tag:topology)

   An object is removed from the matching set unless it is directly linked to all objects with an id (``dataset:as_rank_online``, ``software:bgpstream``) in the search query.
   It's important to note that an object's id is not its type and name, but its type and shortName.
   For example, the dataset "How to Parse CYMRU Bogan Data"'s short name is "bogons" so it's id is "dataset:bogon-cymru-dumps".

    - **-id** (-tag:topology)

       A **-** in front of the id, reverse it's meaning and removes objects from the matching set if it is linked against the object.

### example search strings

|  search string | explanation | 
|----------------|-------------|
| ``types=dataset topology`` | search for datasets with the word 'topology' in a text field |
| ``asn`` | search for all objects with the word 'asn' in a text field |
| ``software:bgpstream`` | search for objects directly linked to the object ``software:bgpstream`` |
| ``bgpstream`` | search for objects with the string "bgpstream" in a field or child's field | 
| ``types=paper,recipe tag:topology`` | search for papers or recipes with the tag 'topology' | 
| ``rank -dataset:as_rank_online`` | searchs for objects with the word rank , not linked to dataset:as_rank_online | 
| ``-caida`` | searchs for objects that do not contain the word caida | 
| ``ids=paper:2021_wie2020_report,media:2020_lvee_online_edition_ithena`` | return the objects with an id 2021_wie2020_report and media:2020_lvee_online_edition_ithena |

