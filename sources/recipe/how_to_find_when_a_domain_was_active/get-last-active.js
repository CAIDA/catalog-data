var apiKey = "YOUR_KEY_HERE";

const fetch = require("node-fetch");

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

// Find when a domain was last active
function getDomainLastActive(domain){
    return dns.get("domains",domain).then((response)=>{
        // If no lastseen is set, domain is still active
        return response.last_seen;
    })    
}

async function run(){
    const googleLastSeen = await getDomainLastActive("google.com");
    console.log(googleLastSeen); // undefined
    const hollow1LastSeen = await getDomainLastActive("hollow1.com");
    console.log(hollow1LastSeen); // 2019-07-09T00:00:00Z
}
run();
