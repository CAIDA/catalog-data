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
            "person": ["person:pillai__vinay", "person:lee__nicole"]
            "organizations": [ "CAIDA, San Diego Supercomputer Center, University of California San Diego" ]
        }
    ]
}
~~~

## **<ins>Introduction</ins>**

The script makes queries to the dzdb api to determine if a domain is still active. The api response contains first-seen and last-seen timestamp properties to which can be used to determine when a domain was last found in a zone file.

## **<ins>Solution</ins>**
The script relies on the below function to handle querying the dzdb api. The dzdb api requres an API key; contact research@dns.coffee to request a key.

~~~
var apiKey = "YOUR_KEY_HERE";

const dns = (function(){
    const baseURL = "https://api.dns.coffee/api/v0";
    const getQueryUrl = (args)=>{
        const urlParts = [baseURL,...args]
        return urlParts.join("/");
    }
    return {
        get(...args){
            return fetch(getQueryUrl(args), {
                method: 'GET',
                headers: {
                    "Accept": 'application/json',
                    "X-API-Key": apiKey
                }
            }).then((response)=>{
                const rootPromise = new Promise(async (rootResolve) => {
                    if(response.ok) {
                        data =  response.json().then((response)=>response.data);
                        rootResolve(data)
                    } else if(response.status == '429') {
                        let delay = response.headers.get('retry-after')*1000 || 2000 // Retry after defaults to 2 seconds
                        // Attempts to retry fetch after delay
                        const promise = new Promise((resolve) => {
                            setTimeout(function() {
                                 data =  dns.get(args.join("/"))
                                 resolve(data)
                            }, delay)    
                        }) 
                        let responseData = await promise;
                        rootResolve(responseData)
                    } else {
                        console.log(response)
                        throw Error("API Query Failed");
                    }
                });
                 return rootPromise; 
            }) 
        },
    }
})();
~~~

This helper function can be used independently for making queries to the API, and simplifies the process of making queries, including the adding of a CORS proxy to the requests. 

~~~
dns.get('domains','google.com'); // Queries https://dns.coffee/api/domains/google.com
dns.get('/domains/google.com'); // Also accepts the format of the link returned in api responses
dns.get('zones','com');
~~~

## **<ins>Background</ins>**
### What is a zone 
A DNS zone is a group of hostnames that is managed by a single individual or organization (Ex. The COM zone is the group of all .com domains).
### What is a zone file
A zone file is a text file which contains the domain, nameserver, ip, and other relationships for the hostnames in a particular zone. DZDB tracks the daily changes to the TLD zone files, and records when a particular domain is first and last seen in the zone files.
