import fetch from "node-fetch";

const dns = (function () {
  const baseURL = "https://dzdb.caida.org/api";
  const getQueryUrl = (args) => {
    const urlParts = [baseURL, ...args];
    return urlParts.join("/");
  };
  return {
    get(...args) {
      return fetch(getQueryUrl(args), {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      }).then((response) => {
        const rootPromise = new Promise(async (rootResolve, rootReject) => {
          if (response.ok) {
            const data = response.json().then((response) => response.data);
            rootResolve(data);
          } else if (response.status == "429") {
            let delay = response.headers.get("retry-after") * 1000 || 2000; // Retry after efaults to 2 seconds
            // Attempts to retry fetch after delay
            const promise = new Promise((resolve) => {
              setTimeout(function () {
                data = dns.get(args.join("/"));
                resolve(data);
              }, delay);
            });
            let responseData = await promise;
            rootResolve(responseData);
          } else {
            console.log(response);
            throw Error("API Query Failed");
          }
        });
        return rootPromise;
      });
    },
  };
})();

// Get all NS and A/AAAA data for a domain
async function getDomainRecords(domain) {
  if (!domain) {
    throw new Error("Domain is required");
  }

  const domainData = await dns.get(`domains/${domain}`);
  const domainNameservers = await dns.get(`domains/${domain}`);
  const zone = await dns.get(`zones/${domainData.zone.name}`);
  domainData.zone = zone;

  const nameserverPromises = domainNameservers.nameservers.map((nameserver) => {
    return dns.get(`nameservers/${nameserver.name}`).then((nameserverData) => {
      // Collect domain and ip data for each nameserver
      let promise = new Promise(async (domainResolve) => {
        const getDomainData = async () => {
          const nameserverInfo = await dns.get(
            `nameservers/${nameserver.name}`
          );

          nameserverData["archive_domains"] = nameserverInfo.archive_domains;
          nameserverData.domains = nameserverInfo.domains;
          nameserverData.ipv4 = nameserverInfo.ipv4;
          nameserverData.ipv6 = nameserverInfo.ipv6;
          return nameserverData;
        };
        const data = await getDomainData();
        domainResolve(data);
      }).then((nameserverDomains) => {
        if (!domainData.nameservers) {
          domainData.nameservers = [];
        }

        domainData.nameservers.push(nameserverDomains);
      });
      return promise;
    });
  });

  return Promise.all(nameserverPromises).then(() => {
    return domainData;
  });
}

async function run() {
  const googleDomainRecords = await getDomainRecords("google.com");
  console.log(JSON.stringify(googleDomainRecords, null, 1));
}
run();
