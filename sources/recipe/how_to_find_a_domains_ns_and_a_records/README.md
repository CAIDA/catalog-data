
# How to use DZDB to get all nameserver and ip records for a domain

~~~json
{
    "id" : "how-to-find-a-domains-ns-and-a-records",
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

The script takes in a domain, makes a series of queries to the dzdb api, and compiles them into a larger response. The final output consists of the initial domain response along with the embedded responses for each of the domain's nameservers. This recipe requires access to the DZDB API, which requres an API Key. You may request an API key by contacting research@dns.coffee. 

## **<ins>Solution</ins>**
The script will return a JavaScript object that contains the nameserver and domain responses for the queried domain. 

~~~javascript
    const googleDomainRecords = await getDomainRecords("google.com");
    console.log(googleDomainRecords); 
~~~

For instance, the above code snippet will output the following object:

~~~

{
  "name": "GOOGLE.COM",
  "nameserver_count": 4,
  "archive_nameserver_count": 0,
  "zone": {
    "name": "COM",
    "nameserver_count": 13,
    "archive_nameserver_count": 0,
    "import_data": {
      "first_date": "2011-04-11T00:00:00Z",
      "last_date": "2021-01-26T00:00:00Z",
      "zone": "COM",
      "records": 372976659,
      "domains": 150301702,
      "count": 3354
    },
    "root": {
      "first_import": "2011-04-11T00:00:00Z",
      "last_import": "2021-01-26T00:00:00Z"
    }
  },
  "nameservers": [
    {
      "name": "NS2.GOOGLE.COM",
      "domain_count": 8768,
      "archive_domain_count": 54076,
      "ipv4_count": 1,
      "archive_ipv4_count": 0,
      "ipv6_count": 1,
      "archive_ipv6_count": 0,
      "archive_domains": [
        {
          "name": "POWERWALLSIAM.COM",
          "first_seen": "2021-01-25T00:00:00Z",
          "last_seen": "2021-01-25T00:00:00Z"
        },
        ...
      ],
     "domains": [
        {
          "name": "PRIVATEBROKE.COM",
          "first_seen": "2021-01-26T00:00:00Z"
        },
        ...
     ],
    "ipv4": [
        {
          "name": "216.239.36.10",
          "version": 4
        }
      ],
      "ipv6": [
        {
          "name": "2001:4860:4802:36::a",
          "version": 6,
          "first_seen": "2018-02-23T00:00:00Z"
        }
      ]
    },
    ...
      ]
    }
  ]
}
    
~~~

The script relies on the below function to handle querying the dzdb api.

~~~
// Simplified API querying object
var apiKey = "YOUR_API_KEY_HERE";

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
                if(response.ok){
                    return response.json().then((response)=>response.data);
                }
                // console.log(response)
                throw Error("API Query Failed");
            });
        },
    }
})();
~~~

This helper function can be used independently for making queries to the API, and simplifies the process of making queries. 

~~~javascript
dns.get('domains','google.com'); // Queries https://dns.coffee/api/domains/google.com
dns.get('/domains/google.com'); // Also accepts the format of the link returned in api responses
dns.get('zones','com');
~~~

## **<ins>Background</ins>**
### What is a zone 
A DNS zone is a group of hostnames that is managed by a single individual or organization (Ex. The COM zone is the group of all .com domains).
### What is a zone file
A zone file is a text file which contains the domain, nameserver, ip, and other relationships for the hostnames in a particular zone. DZDB tracks these relationships, and makes it possible to query for all the nameservers associated with a given domain, as well as all the ips associated with those nameservers.
