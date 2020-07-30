~~~json
{
    "id":"solution:how_to_annotate_an_ark_traceroute_with_hostnames",
    "visibility": "public",
    "name": "How to annotate an ark traceroute with hostnames?",
    "description":"",
    "links": [{}],
    "tags": [
    ]
}
~~~
## **<ins> Introduction </ins>**
The solution parses the ark warts file and merges it with the corresponding ip2hostname file.


### Explanation of the data fields ###
#### IPv4 Prefix-Probing Traceroute Dataset
These data result from CAIDA's traceroute-based measurements running on the Archipelago (Ark) measurement infrastructure (also see CAIDA's Macroscopic Topology Project). We use BGPStream to gather announced BGP prefixes from RIPE and RouteViews BGP data. Each day, we derive a new set of announced prefixes using a sliding window of 7 days of BGP data (7 days of data ending on the day on which a daily BGP prefix set is generated). For each announced prefix, we generate a single target address, ensuring there is never more than one target address in any prefix despite the presence of overlapping prefixes (that is, more specific prefixes).
Download dataset [here](https://www.caida.org/data/active/ipv4_prefix_probing_dataset.xml)

#### The IPv4 Routed /24 Topology Dataset
This dataset contains information useful for studying the topology of the Internet. Data is collected by a globally distributed set of Ark monitors. The monitors use team-probing to distribute the work of probing the destinations among the available monitors.

We collect data by sending scamper probes continuously to destination IP addresses. Destinations are selected randomly from each routed IPv4 /24 prefix on the Internet such that a random address in each prefix is probed approximately every 24 hours (one probing cycle). Because team-probing distributes the probing work across all monitors, a single destination /24 will be probed by only one monitor in each probing cycle.
Download dataset [here](https://www.caida.org/data/active/ipv4_routed_24_topology_dataset.xml)

#### Ark IPv6 Topology Dataset
Download dataset [here](https://www.caida.org/data/active/ipv6_allpref_topology_dataset.xml)

#### IPv4 Routed /24 DNS Names Dataset
The IPv4 Routed /24 DNS Names dataset provides fully-qualified domain names for IP addresses seen in the traces of the IPv4 Routed /24 Topology Dataset.
We also provide the DNS query and response traffic resulting from the DNS lookups required to construct the DNS Names dataset.
Download dataset [here](https://www.caida.org/data/active/ipv4_dnsnames_dataset.xml)

#### The IPv6 DNS Names Dataset
The IPv6 DNS Names dataset provides fully-qualified domain names for IPv6 addresses seen in the traces of the IPv6 Topology Dataset.
Download dataset [here](https://www.caida.org/data/active/ipv6_dnsnames_dataset.xml)

## **<ins> Solution </ins>**
The following script returns a dictionary 

**usage**: `parse_ark_traceroute.py -w [warts file] -i [dns file]`
 ~~~python
import argparse
import re
import warts
from warts.traceroute import Traceroute

directory = "../../../../dataset/" #add file name behind

parser = argparse.ArgumentParser()
parser.add_argument("-t", type=str, dest="traceroute_file", default=None, help="Please enter the file name of warts file")
parser.add_argument("-d", type=str, dest="dns_file", default=None, help="Please enter the file name of ip2hostname file") 
args = parser.parse_args()

re_warts = re.compile(r".warts$")
re_txt = re.compile(r".txt$")
re_ipv4_traceroute = re.compile(r"team-probing")
re_ipv6_traceroute = re.compile(r"topo-v6.l8")
re_ipv4_dns = re.compile(r"dns-names.l7")
re_ipv6_dns = re.compile(r"dns-names.l8")

if not re_warts.search(args.traceroute_file):
    print("The file type of the first argument should be .warts")
elif not re_txt.search(args.dns_file):
    print("The file type of the second argument should be .txt")
elif re_ipv4_traceroute.search(args.traceroute_file) and re_ipv6_dns.search(args.dns_file):
    print("Parsing Ipv4 traceroute file should use Ipv4 DNS file")
elif re_ipv6_traceroute.search(args.traceroute_file) and re_ipv4_dns.search(args.dns_file):
    print("Parsing Ipv6 traceroute file should use Ipv6 DNS file") 
else:

    traceroute = []
    dns = {}

    # reading DNS file
    with open(directory + args.dns_file) as f:
        for line in f:
            line = line.split()
            if len(line)==2:
                continue
            elif line[2] == "FAIL.SERVER-FAILURE.in-addr.arpa" or line[2] == "FAIL.NON-AUTHORITATIVE.in-addr.arpa":
                continue
            else:
                dns[line[1]] = line[2]

    with open(directory + args.traceroute_file, 'rb') as f:

        traceroute_list = []
        while True:
            record = warts.parse_record(f)
            if record == None:
                break
            if isinstance(record, Traceroute):
                if record.src_address:
                    if record.src_address in dns:
                        traceroute_list.append(record.src_address + ":" +dns[record.src_address])
                    else:
                        traceroute_list.append(record.src_address)
                
                for h in record.hops:
                    if h.address in dns:
                        traceroute_list.append(h.address + ":" + dns[h.address])
                    else:
                        traceroute_list.append(h.address)

                if record.dst_address:
                    if record.dst_address in dns:
                        traceroute_list.append(record.dst_address + ":" + dns[record.dst_address])
                    else:
                        traceroute_list.append(record.dst_address)
                traceroute.append(traceroute_list)
            
~~~
##  **<ins> Background </ins>**

### What is a Traceroute?
Traceroute is a computer network diagnostic command for displaying possible routes (paths) and measuring transit delays of packets across an Internet Protocol (IP) network.The history of the route is recorded as the round-trip times of the packets received from each successive host (remote node) in the route (path); the sum of the mean times in each hop is a measure of the total time spent to establish the connection. Traceroute proceeds unless all (usually three) sent packets are lost more than twice; then the connection is lost and the route cannot be evaluated. Ping, on the other hand, only computes the final round-trip times from the destination point.
From [Wikipedia](https://en.wikipedia.org/wiki/Traceroute)


 
### What is Scamper?
Scamper is designed to actively probe destinations in the Internet in parallel (at a specified packets-per-second rate) so that bulk data can be collected in a timely fashion. Scamper's native output file format is called warts: a warts file contains substantial meta data surrounding each individual measurement conducted, as well as substantial detail of responses received. The measurements conducted can range from simple to complex. An example of a simple measurement is where a single measurement method (e.g. traceroute) is used on a list of IP addresses to conduct a bulk measurement. A more complex measurement might be where the outcome of a previous test influences what happens next: for example, for each hop in a traceroute path, infer the address of the outgoing interface for the previous hop. Complex measurements are conducted by connecting to a running scamper process with a driver program which contains the logic.

Download source code from [here](https://www.caida.org/tools/measurement/scamper/code/scamper-cvs-20200717.tar.gz)   

    
### <ins> Caveats </ins>



