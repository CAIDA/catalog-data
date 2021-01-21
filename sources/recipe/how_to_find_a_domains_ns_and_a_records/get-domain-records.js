// var apiKey = "YOUR_API_KEY_HERE";

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
                if(response.ok){
                    return response.json().then((response)=>response.data);
                }
                // console.log(response)
                throw Error("API Query Failed");
            });
        },
    }
})();

// Get all NS and A/AAAA data for a domain
async function getDomainRecords(domain){
    const domainData = await dns.get(`domains/${domain}`);
    const domainNameservers = await dns.get(`/domains/${domain}/nameservers/current`)
    const nameservers = [];

    dns.get("zones", domainData.zone).then((zoneData) => {domainData.zone = zoneData})

    const nameserverPromises = domainNameservers.map((nameserver) => {
        return dns.get(`/nameservers/${nameserver.name}`).then((nameserverData) => {
            nameservers.push(nameserverData)  
            // dns.get(`/nameservers/${nameserverData.name}/domains/current`).then((nameserverDomain) => {
            //     nameserverData.domains = nameserverDomain
            // })

        })
    })



    return Promise.all(nameserverPromises).then(() => {
        domainData.response = nameservers
    }).then(() => {
        return domainData
    })    
}

async function run(){
    const googleDomainRecords = await getDomainRecords("example.com");
    console.log(googleDomainRecords); 
}
run();



// const nameserverPromises = []
// const nameservers = []
// const nameserverList = new Promise((resolve, reject) => {
//     domainNameservers.forEach((nameserver)=>{
//         nameserverPromises.push(dns.get(`/nameservers/${nameserver.name}`)
//             .then((nameserverData)=>{
//                 nameserver.response = nameserverData;
//                 return nameserver
//             }).then((nameserver) => {
//                 nameservers.push(nameserver).then((nameservers) => {
//                     resolve(nameservers)
//                 })
//             }).catch((error)=>{
//                 nameserver.hazardous=true;
//             }));
//         })
//     });

// nameserverList.then((nameservers) => {
//     domainData.nameservers = nameservers
//     console.log(domainData)
// })

// return domainData;
