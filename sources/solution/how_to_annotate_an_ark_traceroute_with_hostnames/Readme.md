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


## **<ins> Solution </ins>**
The following script returns a dictionary 

**usage**: `parse_ark.py -n nodes.bz2 -l links.bz2 -a nodes.as.bz2 -g nodes.geo.bz2`
 ~~~python
import argparse
            
~~~
##  **<ins> Background </ins>**

### What is a Traceroute?
Traceroute is a computer network diagnostic command for displaying possible routes (paths) and measuring transit delays of packets across an Internet Protocol (IP) network.The history of the route is recorded as the round-trip times of the packets received from each successive host (remote node) in the route (path); the sum of the mean times in each hop is a measure of the total time spent to establish the connection. Traceroute proceeds unless all (usually three) sent packets are lost more than twice; then the connection is lost and the route cannot be evaluated. Ping, on the other hand, only computes the final round-trip times from the destination point.
From [Wikipedia](https://en.wikipedia.org/wiki/Traceroute)


 
### What is Scamper?
Scamper is designed to actively probe destinations in the Internet in parallel (at a specified packets-per-second rate) so that bulk data can be collected in a timely fashion. Scamper's native output file format is called warts: a warts file contains substantial meta data surrounding each individual measurement conducted, as well as substantial detail of responses received. The measurements conducted can range from simple to complex. An example of a simple measurement is where a single measurement method (e.g. traceroute) is used on a list of IP addresses to conduct a bulk measurement. A more complex measurement might be where the outcome of a previous test influences what happens next: for example, for each hop in a traceroute path, infer the address of the outgoing interface for the previous hop. Complex measurements are conducted by connecting to a running scamper process with a driver program which contains the logic.

Download source code from [here](https://www.caida.org/tools/measurement/scamper/code/scamper-cvs-20200717.tar.gz)   

    
### <ins> Caveats </ins>



