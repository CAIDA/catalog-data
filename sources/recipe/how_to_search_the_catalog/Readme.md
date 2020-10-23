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

| type | meaning | examples |
|------|------------|---------|
| **key/value** ``(key)=(value)`` | a key and a value pair  | types=dataset,recipe | 
| **id**      ``(type):(shortName)``  | an object id | dataset:asrank , tag:asn | 
| **-id**      ``-(type):(shortName)``  | an object id | -dataset:asrank , -tag:asn | 
| **word**      | anything that doesn't match the above |
| **-word**      | anything that doesn't match the above |

- **words** (rank)

   An object is added to the matching set if it contains all the supplied words in a text field (''name'', ''organization'', etc) or 
   a child's text field ("paper's author's organization"). If no words are provided, all objects are added to the matching set.

    - **-word** (-rank)

       A **-** in front of the word. Reverse it's meaning and removes objects from the matching set if the word is found in a field.

- **key/value pairs** (types=paper,dataset)

   Currently the catalog only support's the key word ``types``.  

   - **Types** is a comma deliminated set of object types (``dataset,recipe``), the *type set*.  Objects are removed from
   the matching set if thier type is not contained in the *type set*.  If types is not provided, all types are considered valid.

      |   key    |    value     | 
      |----------|--------------|
      |   types  |   comma separated list of target types <br>  `types=dataset`  &nbsp;&nbsp;&nbsp;  `types=media,recipe` | 
      
- **ids** (tag:topology)

   An object is removed from the matching set unless it is directly linked to all objects with an id (``dataset:asrank``, ``software:bgpstream``) in the search query.
   It's important to note that an object's id is not its type and name, but its type and shortName.
   For example, the dataset "How to Parse CYMRU Bogan Data"'s short name is "bogons" so it's id is "dataset:bogons".

    - **-id** (-tag:topology)

       A **-** in front of the id. Reverse it's meaning and removes objects from the matching set if it is linked against the object.

### example search strings

|  search string | explination | 
|----------------|-------------|
| ``types=dataset topology`` | search for datasets with the word 'topology' in a text field |
| ``asn`` | search for all objects with the word 'asn' in a text field |
| ``recipe=paper,recipe tag:topology`` | search for papers or recipes with the tag 'topology' | 

