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

// Find when a domain was last active
function getDomainLastActive(domain){
    return dns.get("domains",domain).then((response)=>{
        // If no lastseen is set, domain is still active
        return response.lastseen;
    })    
}

async function run(){
    const googleLastSeen = await getDomainLastActive("google.com");
    console.log(googleLastSeen); // undefined
    const hollow1LastSeen = await getDomainLastActive("hollow1.com");
    console.log(hollow1LastSeen); // 2019-07-09T00:00:00Z
}
run();