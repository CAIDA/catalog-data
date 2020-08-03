~~~
{
    "id": "how_to_annotate_an_ark_traceroute_with_hostnames",
    "visibility": "public",
    "name": "How to annotate an ark traceroute with hostnames?",
    "description": " ",
    "links": [{}],
    "tags": [
    ]
}
~~~
## **<ins> Introduction </ins>**
The solution parses traceroutes from ark warts file and annotates IP addresses with hostnames from ip2hostname file. 

## **<ins> Solution </ins>**
Below is the method in `parse_ark_traceroute.py`used to load IP addressses with corresponding hostnames into the dictionary `dns` with the following format:`{'ip address': 'hostname'}`.
 ~~~python
# reading DNS file
def load_dns_file(dns_file):
    global dns
    with open(dns_file) as f:
        for line in f:
            line = line.split()
            if len(line)==2:
                continue
            elif line[2] == "FAIL.SERVER-FAILURE.in-addr.arpa" or line[2] == "FAIL.NON-AUTHORITATIVE.in-addr.arpa":
                continue
            else:
                dns[line[1]] = line[2]
~~~

Below is the method used to parse .warts file and return the IP address and hostname of a traceroute in list format. Note that set `single_IP` to False to return all IPs in a hop if the hop has multiple IPs. Set `single_IP` to True to return only one IP.
The return format: `['source', 'hop_1', 'hop_2', ... , 'hop_n', 'destination']`
~~~python
def parse_trace(trace, single_IP=False):
    global dns
    ips = []
    hostnames = []

    if trace.src_address:
        ips.append(trace.src_address)
        if trace.src_address in dns:
            hostnames.append(dns[trace.src_address])
        else:
            hostnames.append(None)

    for h in trace.hops:
        if single_IP:
            if len(h.address.split(','))>=2:
                ips.append(None)
                hostnames.append(None)
                input("There are at least two ip addresses in a hop")
            else: # sinle ip in a hop
                ips.append(list(h.address))
                if h.address in dns:
                    hostnames.append()
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
From [Wikipedia](https://en.wikipedia.org/wiki/Traceroute)

### What is Scamper?
Scamper is designed to actively probe destinations in the Internet in parallel (at a specified packets-per-second rate) so that bulk data can be collected in a timely fashion. Scamper's native output file format is called warts: a warts file contains substantial meta data surrounding each individual measurement conducted, as well as substantial detail of responses received. The measurements conducted can range from simple to complex. An example of a simple measurement is where a single measurement method (e.g. traceroute) is used on a list of IP addresses to conduct a bulk measurement. A more complex measurement might be where the outcome of a previous test influences what happens next: for example, for each hop in a traceroute path, infer the address of the outgoing interface for the previous hop. Complex measurements are conducted by connecting to a running scamper process with a driver program which contains the logic.

Download source code from [here](https://www.caida.org/tools/measurement/scamper/code/scamper-cvs-20200717.tar.gz)   

### Dataset ###
#### IPv4 Prefix-Probing Traceroute Dataset
More information and download dataset [here](https://www.caida.org/data/active/ipv4_prefix_probing_dataset.xml)

#### The IPv4 Routed /24 Topology Dataset
More information and download dataset [here](https://www.caida.org/data/active/ipv4_routed_24_topology_dataset.xml)

#### Ark IPv6 Topology Dataset
More information and download dataset [here](https://www.caida.org/data/active/ipv6_allpref_topology_dataset.xml)

#### IPv4 Routed /24 DNS Names Dataset
More information and download dataset [here](https://www.caida.org/data/active/ipv4_dnsnames_dataset.xml)

#### The IPv6 DNS Names Dataset
More information and download dataset [here](https://www.caida.org/data/active/ipv6_dnsnames_dataset.xml)
    
### <ins> Caveats </ins>
Note that there could be multiple IP addresses to a single hop. So there are two versions. Return nested arraies or return None

Support multiple IPs:
~~~    
ips, hostnames = parse_trace(trace,single_IP=False)

# Return format
ips == [["10.1.2.3"],[],["10.0.0.1","2.1.1.2"]]
hostnames: [["www.caida.org"],[],["cat.caida.org",None]]
~~~

Support only single IP:
~~~
# If a hop has multiple IPs, it should put in a None value
ips, hostnames = parse_trace(trace,single_IP=True)

# Return format
ips == ["10.1.2.3", None, None]
hostnames: ["www.caida.org", None, None]
~~~



