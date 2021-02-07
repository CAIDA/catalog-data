var apiKey = "YOUR_API_KEY_HERE";

const fetch = require("node-fetch");
const chai = require("chai");

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

// Assertion style
chai.should()

/** 
 * DOMAIN
 * */

describe('domains', () => {

    domain = 'google.com'

    /** 
     * domain 
     * */

    describe('GET /domains', () => {
        it('resolves', async () => {
            const result = await dns.get(`domains/${domain}`);

            result.should.have.property('nameserver_count').eq(4);
            result.should.have.property('archive_nameserver_count').eq(0);
            result.should.have.property('zone').eq('COM');
        })
    })

    /** 
     * nameservers archive
     * */

    describe('GET /domains/{domain}/nameservers/archive', () => {
        it('resolves', async () => {

            const result = await dns.get(`domains/${domain}/nameservers/archive`);

            result.should.have.lengthOf(0);
        })
    })

    /** 
     * nameservers current
     * */

    describe('GET /domains/{domain}/nameservers/current', () => {
        it('resolves', async () => {

            const result = await dns.get(`domains/${domain}/nameservers/current`);

            result.should.have.lengthOf(4);
        })
    })

    /** 
     * random
     * */
    describe('GET /random', () => {
        it('resolves', async () => {

            const result = await dns.get(`random`);
            result.should.have.property('name');
        })
    })
})

/** 
 * IP
 * */

describe('ip', () => {

    ip = '127.0.0.1'

    /** 
     * ip
     * */

    describe('GET /ip', () => {
        it('resolves', async () => {
            const result = await dns.get(`ip/${ip}`);

            result.should.have.property('nameserver_count').eq(275);
            result.should.have.property('archive_nameserver_count').eq(600);
            result.should.have.property('version').eq(4);
        })
    })

    /** 
     * nameservers archive
     * */

    describe('GET /ip/{ip}/nameservers/archive', () => {
        it('resolves', async () => {

            const result = await dns.get(`ip/${ip}/nameservers/archive?limit=1000`);

            result.should.have.lengthOf(600);
        })
    })

    /** 
     * nameservers current
     * */

    describe('GET /ip/{ip}/nameservers/current', () => {
        it('resolves', async () => {

            const result = await dns.get(`ip/${ip}/nameservers/current?limit=1000`);

            result.should.have.lengthOf(275);
        })
    })
})


/** 
 * NAMESERVERS
 * */

describe('nameservers', () => {

    nameserver = 'NS1.GOOGLE.COM'

    /** 
     * nameservers
     * */

    describe('GET /nameservers', () => {
        it('resolves', async () => {
            const result = await dns.get(`nameservers/${nameserver}`);

            result.should.have.property('domain_count').eq(8867);
            result.should.have.property('archive_domain_count').eq(54830);
            result.should.have.property('ipv4_count').eq(1);
            result.should.have.property('archive_ipv4_count').eq(0);
            result.should.have.property('ipv6_count').eq(1);
            result.should.have.property('archive_ipv6_count').eq(0);
        })
    })

    /** 
     * domains archive
     * */

    describe('GET /domains/archive', () => {
        it('resolves', async () => {
            const result = await dns.get(`nameservers/${nameserver}/domains/archive?limit=60000`);
            result.should.have.lengthOf(54830);
        }).timeout(3000)
    })

    /** 
     * domains current
     * */

    describe('GET /domains/current', () => {
        it('resolves', async () => {
            const result = await dns.get(`nameservers/${nameserver}/domains/current?limit=9000`);
            result.should.have.lengthOf(8867);
        })
    })

    /** 
     * ipv4 archive
     * */

    describe('GET /ipv4/archive', () => {
        it('resolves', async () => {
            const result = await dns.get(`nameservers/${nameserver}/ipv4/archive`);

            result.should.have.lengthOf(0);
        })
    })

    /** 
     * ipv4 current
     * */

    describe('GET /ipv4/current', () => {
        it('resolves', async () => {
            const result = await dns.get(`nameservers/${nameserver}/ipv4/current`);

            result.should.have.lengthOf(1);
        })
    })

    /** 
     * ipv6 archive
     * */

    describe('GET /ipv6/archive', () => {
        it('resolves', async () => {
            const result = await dns.get(`nameservers/${nameserver}/ipv6/archive`);

            result.should.have.lengthOf(0);
        })
    })

    /** 
     * ipv6 current
     * */

    describe('GET /ipv6/current', () => {
        it('resolves', async () => {
            const result = await dns.get(`nameservers/${nameserver}/ipv6/current`);

            result.should.have.lengthOf(1);
        })
    })

})


/** 
 * ZONES
 * */

describe('zones', () => {

    zone = 'net'

    /** 
     * zones
     * */

    describe('GET /zones', () => {
        it('resolves', async () => {
            const result = await dns.get(`zones/${zone}`);
            
            result.should.have.property('nameserver_count').eq(13);
            result.should.have.property('archive_nameserver_count').eq(0);
            result.should.have.property('import_data').property('records').eq(33955427);
            result.should.have.property('import_data').property('domains').eq(13143595);
            result.should.have.property('import_data').property('count').eq(3430);
            result.should.have.property('import_data').property('first_date').eq("2011-04-11T00:00:00Z");
            result.should.have.property('import_data').property('last_date').eq("2021-02-06T00:00:00Z");

        })
    })

    /** 
     * nameservers archive
     * */

    describe('GET /zones/{zone}/nameservers/archive', () => {
        it('resolves', async () => {
            const result = await dns.get(`zones/${zone}/nameservers/archive`);

            result.should.have.lengthOf(0);
        })
    })

    /** 
     * nameservers current
     * */

    describe('GET /zones/{zone}/nameservers/current', () => {
        it('resolves', async () => {
            const result = await dns.get(`zones/${zone}/nameservers/current`);

            result.should.have.lengthOf(13);
        })
    })
})
