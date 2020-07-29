## How to parse ipv6 AS links ##
~~~
{
    "name": "How to parse arks ipv6 as links?",
    "descriptions": ""
    "links": ["software:pyasn","software:scamper", "dataset:ipv6_aslinks_dataset", "dataset:as_prefix"],
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




## <ins> Solution </ins> ## 

Mapping ipv6 addresses to asns


## <ins> Background </ins> ## 

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

`$ pip install pyasn -- pre`

Or with the standard python:

`$ python setup.py build`\
`$ python setup.py install --record log`

You will need to have pip, setuptools and build essentials installed if you build the package manually. On Ubuntu/Debian you can get them using the following command:

`$ sudo apt-get install python-pip python-dev build-essential`

Detailed installation instructions and more information on Usage and IPASN data files [found here]( https://github.com/hadiasghari/pyasn ).



## <ins> Caveats </ins> ##
• **Multi-origin AS**: A multi-origin AS occurs when a given BGP prefix is announced by more than one AS.  Suppose some prefix 10.0.0.0/8 is announced in the BGP table by both AS 10 and AS 20. Then an address in that prefix, like 10.0.0.1, will map to both AS 10 and AS 20.  This is indicated by using the pseudo AS number 10_20.  If AS 30 also announces that prefix, then you would see 10_20_30.
