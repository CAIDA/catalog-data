## How to parse through ark IPv4/IPv6 traceroutes
~~~json
{
    "id": "how_to_parse_ark_traces",
    "visibility": "public",
    "name": "How to parse through an ark traceroute?",
    "description": "This script parses an ark warts file using json to annotate a simple traceroute IP path.",
    "links": [{
        "to": "dataset:ipv4_prefix_probing_dataset",
        "to": "dataset:ipv4_routed_24_topology_dataset",
        "to": "dataset:ipv6_allpref_topology",
        "to": "dataset:ipv6_routed_48_topology_dataset"
        }],
    "tags": [
        "topology",
        "software/tools",
        "IPv4",
        "IPv4 prefix",
        "IPv6",
        "json",
        "parsing",
        "warts",
        "traceroute"
    ],
    "authors":[
        {
            "person": "zabegalin__sasha",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## Introduction

The following solution parses through an [arks ipv4/ipv6 warts files](https://www.caida.org/catalog/datasets/request_user_info_forms/ark ) and produces a simple traceroute in the following order: src, ip1, ip2, ip3..ipn, dst where ip1 - ipn are listed in increasing order of probe-ttl values

**Example Usage:** 
~~~bash 

$ sc_warts2json < .warts file > | python parse_trace_routes.py 
~~~

### Methods  
simple_ip_path() takes in one input: 
• `ark_trace`: This is a single line in the the json file produced as a result of running the [sc_warts2json](https://www.caida.org/catalog/software/scamper/man/sc_warts2json.1.pdf) method on a [warts file]( https://www.caida.org/catalog/datasets/request_user_info_forms/ark)

~~~python
def simple_ip_path(ark_trace):
    
    simple_trace_path_text = '-> traceroute to {} ({}), {} hops max, {} byte packets\n'
    simple_hop_path_text = '\t{}) Hop Address: {} ({}) | RTT: {:.3f} ms'
    
    trace_dst_ip = ark_trace['dst']
    trace_dst_name = socket.getfqdn(ark_trace['dst'])
    trace_hop_count = ark_trace['hop_count']
    trace_byte_packets = ark_trace['probe_count']
    
    path_counter = 1
    
    print(simple_trace_path_text.format(trace_dst_name, trace_dst_ip, 
                                        trace_hop_count, trace_byte_packets))
    print('{')
    
    hops = ark_trace['hops']
    
    for hop in hops:
        
        hop_addr_ip = hop['addr']
        hop_addr_name = socket.getfqdn(hop['addr'])
          
        hop_rtt = hop['rtt']
        
        print(simple_hop_path_text.format(path_counter, hop_addr_name, hop_addr_ip, hop_rtt))
        path_counter += 1
    
    print('}')
~~~


## Background 

### What is a Traceroute?
Traceroute is a computer network diagnostic command for displaying possible routes (paths) and measuring transit delays of packets across an Internet Protocol (IP) network.
More information can be found on [Wikipedia](https://en.wikipedia.org/wiki/Traceroute)

### TTL 
TTL stands for Time To Live. When a TCP packet is sent, its TTL is set, which is the number of routers (hops) it can pass through before the packet is discarded. As the packet passes through a router the TTL is decremented until, when the TTL reaches zero, the packet is destroyed and an ICMP "time exceeded" message is returned. The return message's TTL is set by the terminating router when it creates the packet, and decremented normally.

More information on TTL can be found [here]( http://users.cs.cf.ac.uk/Dave.Marshall/Internet/node77.html ). 

### Trace data
| field | definition | 
|------|-----------|
| version | warts version used for the file |
| type | type of warts data collected | 
| userid | unset user id |
| method | method to collect the data |
| | |
| src | source: IP address of the target of trace |
| dst | destination: IP address of the target of the trace |
| icmp_sum | sum of error-reporting protocols used for the checksum to see if the ICMP header is corrupt or not|
| stop_reason | reason trace stopped |
| stop_data | data that stopped trace |

#### Trace [start] data
| field | definition | 
|------|-----------|
| start | stores 3 types of start times |
| sec | start time in seconds |
| usec | start time in microseconds |
| ftime | start time in full date/time format |

#### Trace Data ll
| field | definition | 
|------|-----------|
| hop_count | max hops in a trace |
| attempts | number of attempts made |
| hoplimit | Specifies the maximum time to live (TTL) or hop limit. The range for valid values is 1 - 255. The default is 30. |
| firsthop | location of the first hop |
| wait | Specifies how long to wait for a response. The range for valid values is 1 - 255. The default is 5 seconds. |
| wait_probe | standard wait time before each probe |
| tos | Specifies the Type of Service value (tos) in the probe packets. The range for valid values is 0 - 255. The default is 0. This parameter applies only to IPv4 destinations and is ignored for IPv6 destinations. |
| probe_size | specifies the size of probes sent |


### Hop Data
| field | definition | 
|------|----------|
| addr | IP address of machine that sent TTL expired message | 
| prob_ttl | This is the TTL set in the probe packet when it left the monitor | 
| probe_size | This is the probe size of the probe packet when it left the monitor |
| rtt | This is the Round-trip time (RTT), the duration, measured in milliseconds, from when the probe packet sent its request to when it receives a response from the monitor |
| reply_ttl | This is the TTL value in the packet that was received by the monitor |
| reply_tos | This is the TOS value in the packet that was received by the monitor |
| reply_size | This is the SIZE value in the packet that was received by the monitor |
| reply_ipid | This is the IP identifier (IP-ID),a 16 (32) bits field in the IPv4 (v6) header [24], in the packet that was received by the monitor |
| icmp_type | This is the type of ICMP message found in the hop |
| icmp_code | This specifies what kind of ICMP message was found in the hop |
| icmp_q_ttl | This is the remaining TTL value after it has been decremented by the intermediate routers |
| icmp_q_ipl | ip length field in the quoted message |
| icmp_q_tos | This is the ICMP's term of service found in the hop |


### What is Scamper?
Scamper is designed to actively probe destinations in the Internet in parallel (at a specified packets-per-second rate) so that bulk data can be collected in a timely fashion. Scamper's native output file format is called warts: a warts file contains substantial meta data surrounding each individual measurement conducted, as well as substantial detail of responses received. The measurements conducted can range from simple to complex. An example of a simple measurement is where a single measurement method (e.g. traceroute) is used on a list of IP addresses to conduct a bulk measurement. A more complex measurement might be where the outcome of a previous test influences what happens next: for example, for each hop in a traceroute path, infer the address of the outgoing interface for the previous hop. Complex measurements are conducted by connecting to a running scamper process with a driver program which contains the logic.

- More information on Scampper can be found [here](https://www.caida.org/catalog/software/scamper/) 
- Download source code from [here](https://www.caida.org/catalog/software/scamper/code/scamper-cvs-20200717.tar.gz) 
- Read Warts format in Python please read [pywarts](https://github.com/drakkar-lig/scamper-pywarts) 

### Dataset
#### IPv4 Prefix-Probing Traceroute Dataset
More information and download dataset [here](https://www.caida.org/catalog/datasets/ipv4_prefix_probing_dataset) 
Directory:` /datasets/topology/ark/ipv4/prefix-probing`

#### The IPv4 Routed /24 Topology Dataset
More information and download dataset [here](https://www.caida.org/catalog/datasets/ipv4_routed_24_topology_dataset) 
Directory: `/datasets/topology/ark/ipv4/probe-data`

#### Ark IPv6 Topology Dataset
More information and download dataset [here](https://www.caida.org/catalog/datasets/ipv6_allpref_topology_dataset) 
`Directory: /datasets/topology/ark/ipv6/probe-data`
