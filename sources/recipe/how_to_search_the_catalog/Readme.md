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

**examples:** "``types=dataset topology``" , "``asn``" , "``recipe=paper,recipe tag:topology``"

One of the primary ways people can interact with the catalog is with a search query. 
A search query is an unordered collection of object ids, key value pairs, and words
that returns a matching set of objects. The search query is generated from the search
field. The search query can be understood to be a set of AND operations.  An object
matches a search query if it matches all parts of the search query. The search query is 
captilization insensitive.

### key/value, ids, and words

First the search field is split into tokens on white space.  Tokens that contain the `=` character are processed as key value pairs (`types=dataset`).
Tokens that contain a `:` character are processed as object ids (`dataset:asrank`). 
All other tokens are processed as words.

| type | meannging | examples |
|------|------------|---------|
| key/value ``(key)=(value)`` | a key and a value pair  | types=dataset,recipe | 
| id      ``(type):(shortName)``  | an object id | dataset:asrank , tag:asn | 
| word      | anything that doesn't match the above |

First the words are processed to find the set of objects that contain all the words 
in a combination of their fields and placed into the matching set. 
If no words are provided, all objects considered to match set.

If object ids are found in the search query, objects are removed from the matching set 
if they do not have a direct link to all the objects with a matching object id. 
It's important to note that an object's id is not its type and name, but its type and shortName.
For example, the dataset "How to Parse CYMRU Bogan Data"'s short name is "bogons" so it's id is "dataset:bogons".

### key/value pairs 
Currently we only support the key word `types`.  If `types` is provided, then it's value is split 
on the `,` character into a set of types and stored in the `types` set.  
If the `types` key is not provided, then all types are placed into the `types` set.  
Objects are removed from the matching set if their type is not in the `types` set.

   |   key    |    value     | 
   |----------|--------------|
   |   types  |   comma separated list of target types <br>  `types=dataset`  &nbsp;&nbsp;&nbsp;  `types=media,recipe` | 

The resulting set of matching objects is returned. 
