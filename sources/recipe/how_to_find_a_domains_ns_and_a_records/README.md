# How to use DZDB to get all nameserver and ip records for a domain

~~~json
{
    "id" : "solution:how-to-find-a-domains-ns-and-a-records",
    "visibility" : "public",
    "name" : "How to use DZDB to get all nameserver and ip records for a domain",
    "description" : "Using the DZDB API, query a domain and get the combined data for its nameservers and ips",
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

The script takes in a domain, makes a series of queries to the dzdb api, and compiles them into a larger response. The final output consists of the initial domain response along with the embedded responses for each of the domain's nameservers.

## **<ins>Solution</ins>**
The script relies on the below function to handle querying the dzdb api. T
```javascript
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
```
This helper function can be used independently for making queries to the API, and simplifies the process of making queries, including the adding of a CORS proxy to the requests. 
```javascript
dns.useCorsProxy = false; // Flag to use CORS proxy for requests (defaults to true)
dns.get('domains','google.com'); // Queries https://dns.coffee/api/domains/google.com
dns.get('/domains/google.com'); // Also accepts the format of the link returned in api responses
dns.get('zones','com');
```
## **<ins>Background</ins>**
### What is a zone 
A DNS zone is a group of hostnames that is managed by a single individual or organization (Ex. The COM zone is the group of all .com domains).
### What is a zone file
A zone file is a text file which contains the domain, nameserver, ip, and other relationships for the hostnames in a particular zone. DZDB tracks these relationships, and makes it possible to query for all the nameservers associated with a given domain, as well as all the ips associated with those nameservers.