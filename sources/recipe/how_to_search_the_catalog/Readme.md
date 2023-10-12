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
| **id**   `(type):(shortName)`  | returns a given id | `dataset:as_rank_online` | 
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
     | status | comma separated list of status types (`complete`,`ongoing`) | 
     | links | comma separated list of object ids or strings <br> `links=paper:2021_wie2020_report,telescope` <br>This searches by neighbor.  Matches are neighbors of the id's object or objects with the string in a field.<br> In this example, it would search for all objects that are related to the 2021 Wie Report OR matches the string "telescope" anywhere in the object.|
     | fields | will match if the object has the field (doi) | 

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
| [links=tag:asn](https://catalog.caida.org/search?query=links=tag:asn) | search for objects that have the tag `asn`|
| [!links=tag:caida](https://catalog.caida.org/search?query=!%20links=tag:caida) | search for objects that **do not** have the tag `caida`|
| [links=tag:topology ark](https://catalog.caida.org/search?query=links=tag:topology%20ark) | search for objects that are tagged topology and have the word `ark` |
| [bgpstream](https://catalog.caida.org/search?query=bgpstream) | search for objects with the word `bgpstream`  | 
| [categories=ip.packet](https://catalog.caida.org/search?query=categories%3Dip.packet) | search for objects with the category `ip.packet` | 
| [links=tag:ipv4 !ipv6](https://catalog.caida.org/search?query=links%3Dtag%3Aipv4%20!links%3Dtag%3Aipv6) | search for objects that have the `ipv4` tag but do not match the word `ipv6` |
| [!links=dataset:as\_relationships\_serial_1 rank](https://catalog.caida.org/search?query=!links=dataset:as_relationships_serial_1%20rank) | it searches for search for objects with the word `rank` that are not linked to dataset:as_relationships_serial_1 | 
| [types=dataset topology](https://catalog.caida.org/search?query=types=dataset%20topology) | search for **datasets** with the word `topology` in a text field |
| [types=dataset topology ark](https://catalog.caida.org/search?query=types=dataset%20topology%20ark) | search for datasets with the word `topology` and `ark` |
| [types=dataset,recipe links=tag:topology !ark](https://catalog.caida.org/search?query=types=dataset,recipe%20links=tag:topology%20!ark) | search for datasets or recipes with the tag `topology` without the word `ark` | 
| [types=dataset access=public](https://catalog.caida.org/search?query=types=dataset%20access=public) | search for datasets that have a public access |
| [types=dataset status=ongoing](https://catalog.caida.org/search?query=types=dataset%20status=ongoing) | search for datasets that have the status `ongoing` |
| [types=paper routing](https://catalog.caida.org/search?query=types=paper%20routing) | search for papers with the word `routing` |
| [types=paper links=tag:best_paper](https://catalog.caida.org/search?query=types=paper%20links=tag:best_paper) | search for papers with the tag `best paper` |
| [types=paper routing !links=tag:caida](https://catalog.caida.org/search?query=types=paper%20routing%20!links=tag:caida) | search for papers with the word `routing` without the tag `caida`|
| [types=paper routing !links=tag:caida dates=2020,2021](https://catalog.caida.org/search?query=types=paper%20routing%20!links=tag:caida%20dates=2020,2021) | search for papers with the word `routing` without the tag `caida` written in 2020 or 2021|
| [types=paper persons=claffy](https://catalog.caida.org/search?query=types=paper%20persons=claffy) | search for papers authored by people with `claffy` in their name |
| [ids=paper:2021\_wie2020\_report](https://catalog.caida.org/search?query=ids=paper:2021_wie2020_report) | search for the object with the id `paper:2021_wie2020_report` |
| [persons=claffy](https://catalog.caida.org/search?query=persons=claffy) | search for objects associated with people with `claffy` in their name |
| [links=person:clark\_\_david](https://catalog.caida.org/search?query=links=person:clark__david) | search for objects directly linked with the person named David Clark |
| [links=person:claffy\_\_kc,person:clark\_\_david](https://catalog.caida.org/search?query=links=person:claffy__kc,person:clark__david) | search for objects linked to `kc claffy` OR `David Clark`|
| [links=person:claffy\_\_kc links=person:clark\_\_david](https://catalog.caida.org/search?query=links=person:claffy__kc%20links=person:clark__david) | search for objects linked to `kc claffy` AND `David Clark`|
| [links=software:bgpstream](https://catalog.caida.org/search?query=links=software:bgpstream) | search for objects directly linked to the object id `software:bgpstream` |
| [links=collection:ucsd\_telescope\_datasets iot](https://catalog.caida.org/search?query=links=collection:ucsd_telescope_datasets%20iot) |  search for all papers that used telescope data to study IoT security |
| [software:bgpstream](https://catalog.caida.org/search?query=software:bgpstream) | search for the object with id `software:bgpstream`|



Copyright (c) 2020 The Regents of the University of California
All Rights Reserved