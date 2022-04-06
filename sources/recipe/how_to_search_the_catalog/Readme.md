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

A search query can be generated from a search string by splitting the string into whitespace-delimited tokens, dividing the tokens into key=value pairs, ids, and words.  **The whitespace-delimited tokens are processed as a boolean "and" operator**, i.e. an object with query with multiple tokens must match all of the requirements in the query.
<style>
    th, td {
        border: 1px solid black;
        padding: 0 0.5em;
    }
</style>

| token type | objects it searches for | examples |
|------|------------|---------|
| **key=value(s)** | one or more values in the key  | `types=paper` <br> `types=dataset,recipe` | 
| **id** , !**id**      `(type):(shortName)`  | a specific object id | `dataset:as_rank_online` <br> `!tag:asn` | 
| **word** , !**word**     | general word or phrase  | `topology` <br> `!ipv4` |

    
- **key=value(s) pairs** 

   Each key/value pair has a single key, which defines the type of value, and a comma separated list of values. **The list of comma-separated values is processed as a boolean "or" operator**, i.e. an object is returned if it matches any of the values. 

     |   key    |    value     | 
     |----------|--------------|
     |   types  |  comma separated list of available object types (dataset, paper, media, recipe, software) <br>  `types=dataset` <br> `types=media,recipe` | 
     |   persons | comma separated list of strings matching part of a person's names <br> `persons=john` (returns all objects associated with a person matching `john` in their name)  |  
     |   ids     | comma separated list of object ids <br> `ids=paper:2021_wie2020_report,media:2020_lvee_online_edition_ithena`  |
     | dates | comma separated list of dates which supports year or year-mon <br> `dates=2014,2015` <br> `dates=2015-03` |
     | access | comma separated list of access links types (`public`, `restricted`, `unavailable`, `commercial`) |
     | links | comma separated list of object ids or strings <br> `links=paper:2021_wie2020_report,telescope` <br>This searches by neighbor.  Matches are neighbors of the id's object or objects with the string in a field.  |

- **id** 

   An object is removed from the matching set unless it is directly linked to all objects with an id (`dataset:as_rank_online`, `software:bgpstream`) in the search query.
   
   It's important to note that an object's id is its `type` and `shortName`.  For convenience, the id is displayed in grey just below the title of each catalog entry's details page.

   For example, the dataset "Bogon files from Cymru"'s short name is "bogon_cymru_dumps" so its id is `dataset:bogon-cymru-dumps`. 

   People (e.g. paper authors or media presenters) are of type `person` with `shortName` of the format `(lastname)__(firstname)`.  For example, objects linked to  David Moore can be matched with the id `person:moore__david`

    - **!id** 

       An exclamation point **!** in front of the id, reverse its meaning and removes objects from the matching set if it is linked to the object.

- **word**

   An object is added to the matching set if it contains all the supplied words in a text field or 
   its child's text field. If no words are provided, all objects are added to the matching set.

    - **!word**

       An exclamation point **!** in front of the word, reverse it's meaning and removes objects from the matching set if the word is found in a field.

### example search strings
Remember, the whitespace-delimited tokens are processed as a boolean "and" operator, but the comma-delimited values in a key=value pair are processed as a boolean "or" operator.

|  search string | explanation | 
|----------------|-------------|
| `tag:asn`| search for objects that have the tag `asn`|
| `!tag:caida`| search for objects that do not have the tag `caida`|
| `tag:topology tag:ark` | search for objects that are tagged topology and ark
| `bgpstream` | search for objects with the word `bgpstream`  | 
| `ipv4 !ipv6` | search for objects that match `ipv4` but do not match the word `ipv6` |
| `rank -dataset:as_rank_online` | search for objects with the word `rank` that are not linked to `dataset:as_rank_online` | 
| `types=dataset topology` | search for datasets with the word `topology` in a text field |
| `types=dataset topology ark` | search for datasets with the word `topology` and `ark` |
| `types=dataset,recipe tag:topology !ark` | search for datasets or recipes with the tag `topology` without the word `ark` | 
| `types=dataset access=public` | search for datasets that are marked as public access |
| `types=paper routing` | search for papers with the word `routing` |
| `types=paper tag:best_paper` | search for papers with the tag `best paper` |
| `types=paper routing !tag:caida` | search for papers with the word `routing` without the tag `caida`|
| `types=paper routing !tag:caida dates=2020,2021` | search for papers with the word `routing` without the tag `caida` written in 2020 or 2021|
| `types=paper persons=claffy` | search for papers authored by people with `claffy` in their name |
| `ids=paper:2021_wie2020_report` | search for the object with the id `paper:2021_wie2020_report` |
| `persons=claffy` | search for objects associated with people with `claffy` in their name |
| `person:moore__david` | search for objects directly linked with the person named David Moore |
| `software:bgpstream` | search for objects directly linked to the object id `software:bgpstream` |
