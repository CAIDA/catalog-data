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
    const googleDomainRecords = await getDomainRecords("google.com");
    console.log(googleDomainRecords); 
}
run();