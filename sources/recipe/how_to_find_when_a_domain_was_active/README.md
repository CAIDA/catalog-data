# How to use DZDB to find when a domain was active

~~~json
{
    "id" : "how-to-find-when-a-domain-was-active",
    "visibility" : "public",
    "name" : "How to use DZDB to find when a domain was active",
    "description" : "Using the DZDB API, query a domain and determine when it was last active",
    "links": [{"to":"dataset:dzdb"},{"to":"software:dzdb_api"}],
    "tags" : [
        "last active",
        "dzdb"
    ],
    "authors":[
        {
            "person": "person:pillai__vinay",
            "organizations": [ "CAIDA, San Diego Supercomputer Center, University of California San Diego" ]
        }
    ]
}
~~~

## **<ins>Introduction</ins>**

The script makes queries to the dzdb api to determine if a domain is still active. The api response contains first-seen and last-seen timestamp properties to which can be used to determine when a domain was last found in a zone file.

## **<ins>Solution</ins>**
The script relies on the below function to handle querying the dzdb api.

~~~
// Simplified API querying object
const dns = (function(){
    const corsProxy = "https://cors-anywhere.herokuapp.com";
    const baseURL = "https://dns.coffee/api";
    const getQueryUrl = (useCorsProxy, args)=>{
        const urlParts = [baseURL,...args]
        if(useCorsProxy){
            urlParts.unshift(corsProxy);
        }
        return urlParts.join("/");
    }
    return {
        get(...args){
            return fetch(getQueryUrl(this.useCorsProxy, args)).then((response)=>{
                if(response.ok){
                    return response.json().then((response)=>response.data);
                }
                throw Error("API Query Failed");
            });
        },
        useCorsProxy:true
    }
})();
~~~

This helper function can be used independently for making queries to the API, and simplifies the process of making queries, including the adding of a CORS proxy to the requests. 

~~~
dns.useCorsProxy = false; // Flag to use CORS proxy for requests (defaults to true)
dns.get('domains','google.com'); // Queries https://dns.coffee/api/domains/google.com
dns.get('/domains/google.com'); // Also accepts the format of the link returned in api responses
dns.get('zones','com');
~~~

## **<ins>Background</ins>**
### What is a zone 
A DNS zone is a group of hostnames that is managed by a single individual or organization (Ex. The COM zone is the group of all .com domains).
### What is a zone file
A zone file is a text file which contains the domain, nameserver, ip, and other relationships for the hostnames in a particular zone. DZDB tracks the daily changes to the TLD zone files, and records when a particular domain is first and last seen in the zone files.
