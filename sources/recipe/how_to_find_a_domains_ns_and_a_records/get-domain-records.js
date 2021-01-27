var apiKey = "YOUR_API_KEY_HERE";

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
                const rootPromise = new Promise(async (rootResolve, rootReject) => {
                    if(response.ok) {
                        data =  response.json().then((response)=>response.data);
                        rootResolve(data)
                    } else if(response.status == '429') {
                        let delay = response.headers.get('retry-after')*1000 || 2000 // Retry after efaults to 2 seconds
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

// Get all NS and A/AAAA data for a domain
async function getDomainRecords(domain){
    const domainData = await dns.get(`domains/${domain}`);
    const domainNameservers = await dns.get(`domains/${domain}/nameservers/current`)
    const zone = await dns.get(`zones/${domainData.zone}`)
    domainData.zone = zone


    const nameserverPromises = domainNameservers.map((nameserver) => {
        return dns.get(`nameservers/${nameserver.name}`)
        .then((nameserverData) => {
            // Collect domain and ip data for each nameserver
            let promise = new Promise(async (domainResolve) => {
                getDomainData = async () => {
                    const archive = await dns.get(`nameservers/${nameserverData.name}/domains/archive`)
                    const current = await dns.get(`nameservers/${nameserverData.name}/domains/current`)
                    const ipv4 = await dns.get(`nameservers/${nameserverData.name}/ipv4/current`)
                    const ipv6 = await dns.get(`nameservers/${nameserverData.name}/ipv6/current`)

                    nameserverData['archive_domains'] = archive
                    nameserverData.domains = current
                    nameserverData.ipv4 = ipv4
                    nameserverData.ipv6 = ipv6 
                    return nameserverData
                }
                data = await getDomainData()
                domainResolve(data)
            }).then((nameserverDomains) => {
                if (!domainData.response) {
                    domainData.response = []
                }

                domainData.response.push(nameserverDomains)

            }); return promise
        }) 
    })


    return Promise.all(nameserverPromises).then(() => {
        return domainData
    })
}

async function run(){
    const googleDomainRecords = await getDomainRecords("example.com");
    console.log(JSON.stringify(googleDomainRecords, null, 1)); 
}
run();