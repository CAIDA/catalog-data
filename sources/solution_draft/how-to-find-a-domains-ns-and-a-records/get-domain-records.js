// Get all NS and A/AAAA data for a domain
async function getDomainRecords(domain){
    const domainData = await dns.get("domains",domain);
    const nameserverPromises = []
    domainData.nameservers.forEach((nameserver)=>{
        nameserverPromises.push(dns.get(nameserver.link).then((nameserverData)=>{
            nameserver.response = nameserverData;
        }).catch((error)=>{
            nameserver.hazardous=true;
        }));
    })
    return domainData;
}

async function run(){
    const googleLastSeen = await getDomainRecords("google.com");
    console.log(googleLastSeen); // undefined
}
run();