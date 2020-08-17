
## How to parse arks ipv6 warts file ##
~~~
{
    "name": "How to parse arks ipv6 warts file?",
    "descriptions": "This solution parses through an arks ipv6 warts file and produces a sorted list of ips and asns."
    "links": ["software:pyasn","software:scamper", "dataset:as_prefix"],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools",
        "asn",
        "ipv6"
        "ipv6 prefix"
    ]
}
~~~


## <ins> Introduction </ins> ##

The following solution parses through an [arks ipv6 warts file](https://www.caida.org/data/request_user_info_forms/ark.xml ) and produces a sorted list of ipv6 addresses and asns. 


## <ins> Solution </ins> ## 

The full script can be found [here]( https://github.com/CAIDA/catalog-data/blob/how_to_parse_arks_ipv6_warts_file/sources/recipe/how_to_parse_arks_ipv6_warts_file/parse_arks_ipv6_warts.py ).

### Datasets ###
• `sc_to_json_file`: This is the json file produced as a result of running the [sc_warts2json](https://www.caida.org/tools/measurement/scamper/man/sc_warts2json.1.pdf) method on a warts file. \
Warts files can be found under /datasets/topology/ark/ipv6/probe-data [here](  https://www.caida.org/data/request_user_info_forms/ark.xml ). \
• `.prefix2as6 file`: Datasets can be downloaded [here]( https://www.caida.org/data/routing/routeviews-prefix2as.xml ). The script can accept both .gz files as well as unzipped .prefix2as6 files. \
• `.dat file`: Name of the .dat file used for ipv6 prefix to AS mapping. 

**Example Usage:** 
~~~bash 

$ gunzip topo-v6.l8.20200101.1577836855.yxu-ca.warts.gz
$ sc_warts2json topo-v6.l8.20200101.1577836855.yxu-ca.warts > test.json 
$ python3 parse_arks_ipv6_warts.py -t test.json -p routeviews-rv6-20200101-1200.pfx2as.gz -d test.dat
~~~

### Methods ### 
create_ips() takes in one input: \
• `sc_to_json_file`: This is the json file produced as a result of running the [sc_warts2json](https://www.caida.org/tools/measurement/scamper/man/sc_warts2json.1.pdf) method on a [warts file]( https://www.caida.org/data/request_user_info_forms/ark.xml).\
Instructions to obtain .json file: 

~~~bash
$ gunzip topo-v6.l8.20200101.1577836855.yxu-ca.warts.gz
$ sc_warts2json topo-v6.l8.20200101.1577836855.yxu-ca.warts > test.json 
~~~
    
    
• Note that ips are listed in the following order: `src, ip1, ip2, ip3..ipn, dst` 
where `ip1 - ipn` are listed in increasing order of probe-ttl values. 

~~~python
def create_ips(sc_to_json_file):
    '''
    Parse JSON object and create list of ip addresses. 
    '''
    global ips

    # Load JSON object in a list 
    data = []
    for line in open(sc_to_json_file, 'r'):
        data.append(json.loads(line)) 

    # Parse through data and create list of ips
    # ips are sorted by increasing probe ttl values 
    for elem in data:
        ips.append(elem['src'])
        hops = elem["hops"]
        for hop in hops:
            ips.append(hop["addr"])
        ips.append(elem['dst'])
    print(ips)
~~~
    
We then create a `pyasn` object from a .prefix2as6 file, iterate through the list of ipv6 addresses and create a list of asns using pyasn's `lookup`.  

The method create_asns() produces the list of asns:
~~~python
def create_asns():
    '''
     Create list of asns from pyasn lookup
    '''
    global ips
    global asn_db 

    asns = []
    for ip in ips:
        try:
            asn, prefix = asn_db.lookup(ip)
        except ValueError:
            print("No corresponding asn for ", ip)
        asns.append(asn)
    # print(asns)

~~~

## <ins> Background </ins> ## 

### Traceroute ###
Traceroute is a computer network diagnostic command for displaying possible routes (paths) and measuring transit delays of packets across an Internet Protocol (IP) network.
More information can be found on [Wikipedia](https://en.wikipedia.org/wiki/Traceroute). 

### TTL ### 
TTL stands for Time To Live. When a TCP packet is sent, its TTL is set, which is the number of routers (hops) it can pass through before the packet is discarded. As the packet passes through a router the TTL is decremented until, when the TTL reaches zero, the packet is destroyed and an ICMP "time exceeded" message is returned. The return message's TTL is set by the terminating router when it creates the packet, and decremented normally.

More information on TTL can be found [here]( http://users.cs.cf.ac.uk/Dave.Marshall/Internet/node77.html ). 


### Traceroute data field description ###

| Data Field       |   Meaning                                                                                        |
| -------------    | -----------------------------------------------------------------------------------------------  |
| probe_ttl        | This is the TTL set in the probe packet when it left the monitor                                 |
| reply_ttl        | This is the TTL value in the packet that was received by the monitor                             |                                          | icmp_ttl         | This is the remaining TTL value after it has been decremented by the intermediate routers.       |
|  icmp_ttl        | This is the remaining TTL value after it has been decremented by the intermediate routers.       | 


### IPv6 address ###
• An *IPv6 address* is a 128-bit unique address that is used to recognize a computer network or a machine. All computers on the same data network share the same IPv6 address.\
• IPv6 addressing is a successor to IPv4 addressing. \
• An IPv4 address is 32 bit, whereas an IPv6 address is 128 bit. \
• **IPv6 Prefix** - The leftmost fields of the IPv6 address contain the prefix, which is used for routing IPv6 packets. \
• IPv6 prefixes have the following format:\
`prefix/length in bits` \
• e.g. Consider the IPv6 address : `2001:db8:3c4d:0015:0000:0000:1a2f:1a2b/48` \
• In this case, 48 is the length of the prefix, i.e. the IPv6 prefix is the first 48 bits of the IP address - `2001:db8:3c4d` \
• More information on IPv6 addresses and prefixes found [here]( https://docs.oracle.com/cd/E19253-01/816-4554/6maoq01nv/index.html ).


### Scamper ###

• The Scamper utility is designed to actively probe destinations in the Internet in parallel (at a specified packets-per-second rate) so that bulk data can be collected in a timely fashion.\
• Scamper's native output file format is called **warts**: a warts file contains substantial meta data surrounding each individual measurement conducted, as well as substantial detail of responses received. \
• Scamper supports both **IPv6** and **IPv4** probing. 

More information on Scamper found [here]( https://www.caida.org/tools/measurement/scamper/
 ).

### pyasn ###
**pyasn** is a Python extension module that enables very fast IP address to Autonomous System Number lookups. Current state and Historical lookups can be done, based on the MRT/RIB BGP archive used as input. 

**pyasn** is different from other ASN lookup tools in that it provides offline and historical lookups. It provides utility scripts for users to build their own lookup databases based on any MRT/RIB archive. This makes pyasn much faster than online dig/whois/json lookups.

#### Installation ####
~~~
$ pip install pyasn -- pre
~~~
Or with the standard python:
~~~
$ python setup.py build
$ python setup.py install --record log
~~~
You will need to have pip, setuptools and build essentials installed if you build the package manually. On Ubuntu/Debian you can get them using the following command:

~~~
$ sudo apt-get install python-pip python-dev build-essential
~~~
Detailed installation instructions and more information on Usage and IPASN data files [found here]( https://github.com/hadiasghari/pyasn ).



## <ins> Caveats </ins> ##
• **Multi-origin AS**: A multi-origin AS occurs when a given BGP prefix is announced by more than one AS. These multi-origin AS are dropped when creating the pyasn object i.e this script ignores multi-origin AS. 
