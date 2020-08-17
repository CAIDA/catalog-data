~~~
{
    "id": "how_to_annotate_an_ark_traceroute_with_hostnames",
    "visibility": "public",
    "name": "How to annotate an ark traceroute with hostnames?",
    "description": "Parsing ark warts file and annotating IPs with the hostnames.",
    "links": [{
        "to": "dataset:ipv4_prefix_probing_dataset",
        "to": "dataset:ipv4_routed_24_topology_dataset",
        "to": "dataset:ipv6_allpref_topology_dataset",
        "to": "dataset:ipv4_dnsnames_dataset",
        "to": "dataset:ipv6_dnsnames_dataset"
        }],
    "tags": [
        "topology",
        "software/tools",
        "IPv4",
        "IPv4 prefix",
        "IPv6"
    ]
}
~~~
## **<ins> Introduction </ins>**
The solution parses traceroutes in ark warts file and annotates IPs with hostnames. 

## **<ins> Solution </ins>**
The full script could be found in [parse_ark_traceroute.py](https://github.com/CAIDA/catalog-data/blob/how_to_annotate_an_ark_traceroute_with_hostnames/sources/solution/how_to_annotate_an_ark_traceroute_with_hostnames/parse_ark_traceroute.py) \
**Usage:** ` python parse_ark_traceroute.py -t <traceroute dataset> -d <dns dataset>` 

Below is the method used to load IPs with corresponding hostnames into the dictionary `dns` with the following format:\
`{'ip address': 'hostname'}`.
 ~~~python
# reading DNS file
def load_dns_file(dns_file):
    global dns
    with open(dns_file) as f:
        for line in f:
            line = line.split()
            if len(line) == 2: # missing hostname
                continue
            elif line[2] == "FAIL.SERVER-FAILURE.in-addr.arpa" or line[2] == "FAIL.NON-AUTHORITATIVE.in-addr.arpa":
                continue
            else:
                dns[line[1]] = line[2]
~~~

Below is the method used to parse .warts file and return a traceroute's `ips` and `hostname` in list format.  The method returns source, each hop and destination of a traceroute in sequence. \
 `[source, hop_1, hop_2, ... , hop_n, destination]`

**Note** that there could be multiple IPs in a hop. 
- Set `single_IP` to True to get None value if there are multiple IPs in a hop. 
- Set `single_IP` to False to get all IPs in each hop. 
For more examples, please read Caveats below.

~~~python
def parse_trace(trace, single_IP=False):
    global dns
    ips = []
    hostnames = []

    # source
    if trace.src_address:
        ips.append(trace.src_address)
        if trace.src_address in dns:
            hostnames.append(dns[trace.src_address])
        else:
            hostnames.append(None)
    # hops
    for h in trace.hops:
        if single_IP:
            if len(h.address.split(',')) >= 2:
                ips.append(None)
                hostnames.append(None)
            else: # sinle ip in a hop
                ips.append(h.address)

                if h.address in dns:
                    hostnames.append(dns[h.address])
                else:
                    hostnames.append(None)
        else: # support multiple ips
            hop_hostnames = []
            hop_ips = h.address.split(',')
            ips.append(hop_ips)
            for ip in hop_ips:
                if ip in dns:
                    hop_hostnames.append(dns[ip])
                else:
                    hop_hostnames.append(None)
            hostnames.append(hop_hostnames)

    # destination
    if trace.dst_address:
        ips.append(trace.dst_address)
        if trace.dst_address in dns:
            hostnames.append(dns[trace.dst_address])
        else:
            hostnames.append(None)
    
    return ips, hostnames
            
~~~

##  **<ins> Background </ins>**

### What is a Traceroute?
Traceroute is a computer network diagnostic command for displaying possible routes (paths) and measuring transit delays of packets across an Internet Protocol (IP) network.
More information can be found on [Wikipedia](https://en.wikipedia.org/wiki/Traceroute)

### What is Scamper?
Scamper is designed to actively probe destinations in the Internet in parallel (at a specified packets-per-second rate) so that bulk data can be collected in a timely fashion. \
Scamper's native output file format is called **warts**: a warts file contains substantial meta data surrounding each individual measurement conducted, as well as substantial detail of responses received. 

- More information on Scampper can be found [here](https://www.caida.org/tools/measurement/scamper/) 
- Download source code from [here](https://www.caida.org/tools/measurement/scamper/code/scamper-cvs-20200717.tar.gz) 
- Read Warts format in Python please read [pywarts](https://github.com/drakkar-lig/scamper-pywarts) 

### Dataset ###
#### IPv4 Prefix-Probing Traceroute Dataset
More information and download dataset [here](https://www.caida.org/data/active/ipv4_prefix_probing_dataset.xml) \
Directory:` /datasets/topology/ark/ipv4/prefix-probing`

#### The IPv4 Routed /24 Topology Dataset
More information and download dataset [here](https://www.caida.org/data/active/ipv4_routed_24_topology_dataset.xml) \
Directory: `/datasets/topology/ark/ipv4/probe-data`

#### Ark IPv6 Topology Dataset
More information and download dataset [here](https://www.caida.org/data/active/ipv6_allpref_topology_dataset.xml) \
`Directory: /datasets/topology/ark/ipv6/probe-data`

#### IPv4 Routed /24 DNS Names Dataset
More information and download dataset [here](https://www.caida.org/data/active/ipv4_dnsnames_dataset.xml) \
Directory: `/datasets/topology/ark/ipv4/dns-names`

#### The IPv6 DNS Names Dataset
More information and download dataset [here](https://www.caida.org/data/active/ipv6_dnsnames_dataset.xml) \
Directory: `/datasets/topology/ark/ipv6/dns-names`

### <ins> Caveats </ins>
Note that there could be multiple IP addresses to a single hop. So there are two versions. 

**Support multiple IPs:** \
Set `single_IP` to False to get all IPs in each hop. 
~~~    
ips, hostnames = parse_trace(trace,single_IP=False)

# Return format
ips == [["10.1.2.3"],[],["10.0.0.1","2.1.1.2"]]
hostnames: [["www.caida.org"],[],["cat.caida.org",None]]
~~~

**Support only single IP:** \
Set `single_IP` to True to get None value if there are multiple IPs in a hop. 
~~~
ips, hostnames = parse_trace(trace,single_IP=True)

# Return format
ips == ["10.1.2.3", None, None]
hostnames: ["www.caida.org", None, None]
~~~



