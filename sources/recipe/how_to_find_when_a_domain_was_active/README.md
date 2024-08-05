# How to use DZDB to find when a domain was active

~~~json
{
    "id" : "how-to-find-when-a-domain-was-active",
    "visibility" : "public",
    "name" : "How to use DZDB to find when a domain was active",
    "description" : "Using the DZDB API, query a domain and determine when it was last active",
    "links": [{"to":"dataset:dzdb"},{"to":"recipe:how_to_find_a_domains_ns_and_a_records"}],
    "tags" : [
        "last active",
        "dzdb"
    ],
    "authors":[
        {
            "person": "person:pillai__vinay",
            "organizations": [ "CAIDA, San Diego Supercomputer Center, University of California San Diego" ]
        },
        {
            "person": "person:lee__nicole",
            "organizations": [ "CAIDA, San Diego Supercomputer Center, University of California San Diego" ]
        }
    ]
}
~~~

## **<ins>Introduction</ins>**

The script makes queries to the DZDB API to determine if a domain is still active. The api response contains first-seen and last-seen timestamp properties to which can be used to determine when a domain was last found in a zone file. This recipe requires the user to fill out a user access form. You may complete the user access form [here](https://www.caida.org/catalog/datasets/request_user_info_forms/dzdb).

## **<ins>Solution</ins>**
The script will return a JavaScript object that contains the domain responses for the queried domain.

~~~
const dns = (function(){
    const baseURL = "https://dzdb.caida.org/api";
    const getQueryUrl = (args)=>{
        const urlParts = [baseURL,...args]
        return urlParts.join("/");
    }
    return {
        get(...args){
            return fetch(getQueryUrl(args), {
                method: 'GET',
                headers: {
                    "Accept": 'application/json'
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
dns.get('domains','google.com'); // Queries https://dzdb.caida.org/api/domains/google.com
dns.get('/domains/google.com'); // Also accepts the format of the link returned in api responses
dns.get('zones','com'); // Queries https://dzdb.caida.org/api/zones/com
~~~

## **<ins>Background</ins>**
### What is a zone 
A DNS zone is a group of hostnames that is managed by a single individual or organization (Ex. The COM zone is the group of all .com domains).
### What is a zone file
A zone file is a text file which contains the domain, nameserver, ip, and other relationships for the hostnames in a particular zone. DZDB tracks the daily changes to the TLD zone files, and records when a particular domain is first and last seen in the zone files.
### Notes on DNS Coffee API
The DZDB API utilized in this recipe aids in querying data from the zone file. Documentation for the API can be found [here](https://dzdb.caida.org/api). Requests are rate-limited. You may request access by filling out the form [here](https://www.caida.org/catalog/datasets/request_user_info_forms/dzdb). To view a more comprehensive usage of the API, visit the "How to use DZDB to get all nameserver and ip records for a domain" recipe.


Copyright (c) 2020 The Regents of the University of California
All Rights Reserved
