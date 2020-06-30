~~~
{
    "question": "How to find the AS path for a IPv4 address with Python?",
    "links": ["software:BGPStream"],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools"
    ]
}
~~~
### <ins> Introduction </ins> ###

**What is an IPv4 address prefix?** \
• An *IP address* is a 32-bit unique address that is used to recognize a computer network or a machine. All computers on   the same data network share the same IP address.\
• An IPv4 address is typically written in decimal format as 4 8-bit fields separated by a period. Eg. 182.24.0.0/18 \
• An *IPv4 address prefix* is the prefix of an IPv4 address. \
• e.g. Consider the IPV4 address : 182.24.0.0/18 \
• In this case, 18 is the length of the prefix. \
• The prefix is the first 18 bits of the IP address. \
• More information on IPv4 addresses can be found [here]( https://docs.oracle.com/cd/E19455-01/806-0916/6ja85399u/index.html#:~:text=The%20IPv4%20address%20is%20a,bit%20fields%20separated%20by%20periods )

**What is forwarding/How does forwarding work?** \
• Fowarding means sending incoming information packets to the appropriate destination interface. This is done by routers with the help of a forwarding table. \
• Routers scan the destination IP prefix and locate a match using a forwarding table to determine the packet's next hop. \
• In cases of prefix overlap, where an incoming IP prefix map may match multiple IP entries in the table, the *Longest Prefix Matching Rule* is used to determine the next hop. 

**What is the Longest Prefix Matching Rule?** \
• Longest Prefix Match is an algorithm to lookup the destination an IP prefix’s next hop from the router. \
It finds the prefix matching the given IP address and returns the corresponding router node.\
• The router which corresponds to the IP address with the longest matching prefix is selected as the destination router node.\
• Consider the following example:
| IP Prefix        |   Router      |
| -------------    | ------------- |
| 192.168.20.16/28 | A             |
| 192.168.0.0/16   | B             |

• For example, for the given incoming IP address:  192.168.20.19 \
• **Node A** is selected as the destination router node as it contains the *longer matching prefix* i.e. 192.168.20.16 \
• Source: [link]( https://www.lewuathe.com/longest-prefix-match-with-trie-tree.html ) \
• More information can be found [here]( https://www.geeksforgeeks.org/longest-prefix-matching-in-routers/ )
 
**What are origin AS?**
• Include short note on origin AS 


### <ins> Caveats </ins> ###
• **Multi-origin AS** : Some prefixes originate from multiple AS's (which could be siblings or distinct organizations).\
This makes it more challenging to interpret the appearance of a matching destination IP address, as the address could be on a router operated by any one of the origin AS's. \
• as_set \
• **Third-party AS's** \
• Include diagram and explanation from https://www.caida.org/publications/papers/2016/bdrmap/bdrmap.pdf


### <ins> Mapping IPv4 addresses to origin AS's </ins> ###

## Explanation of dataset ##
~~~
10.2.1.0/24  10 2 3 5  5
10.2.1.0/24  23 5      5
10.2.1.0/24  23 4 5    5
10.2.1.0/24  21 8 4    4
10.2.1.0/24  21 8 {4,3}   as set

10.2.1.0/24 4_5 multie origi
10.2.1.0/24  4_{4,3}
~~~
## PyBGPStream ##

PyBGPStream is a Python library that provides a high-level interface for live and historical BGP data analysis. See http://bgpstream.caida.org for more information about BGPStream. 

PyBGPStream provides two Python modules, `_pybgpstream`, a low-level (almost) direct interface to the [libBGPStream]( https://bgpstream.caida.org/ ) C API, and `pybgpstream`, a high-level 'Pythonic' interface to the functionality provided by `_pybgpstream`. 

### Quick Start ###
To get started using PyBGPStream, first [install libBGPStream]( https://bgpstream.caida.org/docs/install/pybgpstream )

Then, you should be able to install PyBGPStream using pip: 

`$ pip install pybgpstream `

Alternatively, to install PyBGPStream from source either clone the [Github repository]( https://github.com/CAIDA/bgpstream
 ) (PyBGPStream is located in the `pybgpstream` subdirectory), or download a [source tarball]( https://bgpstream.caida.org/download ) and then run:
 
 `$ python setup.py build`\
 `$ python setup.py install`
 
 For more information on installing PyBGPStream, please see the detailed [installation instructions]( https://bgpstream.caida.org/docs/install/pybgpstream ) on the BGPStream website. 
 
 Please see the [PyBGPStream API documentation]( https://bgpstream.caida.org/docs/api/pybgpstream ) and the [PyBGPStream tutorial]( https://bgpstream.caida.org/docs/tutorials/pybgpstream ) for more information about using PyBGPStream.

# solution #
1. Write a script that uses BGPStream's [PyBGPStream](https://bgpstream.caida.org/docs/tutorials/pybgpstream)
to download and store the AS path and prefixes into prefix-as_paths.dat.  Write a script using
[pyasn](https://pypi.org/project/pyasn/) that loads prefix-as_paths.dat, and then use it to map
between the prefix-as_paths.dat and your ips. Below are the relavent code snippets.
 *include short description of BGPStream*
### download Prefix ASN with BGPStream
~~~python
#!/usr/bin/env python

import pybgpstream
stream = pybgpstream.BGPStream(
    from_time="2017-07-07 00:00:00", until_time="2017-07-07 00:10:00 UTC",
    collectors=["route-views.sg", "route-views.eqix"],
    record_type="updates"
)

for elem in stream:
    # record fields can be accessed directly from elem
    asn_path = elem.fields["as-path"]
    prefix = elem.fields["prefix"]
    print(prefix+"\t"+asn_path)
~~~

''' python3 ip_asn.py -p prefix2asn.dat -i ips.txt -m pyasn '''
### code snippit 
~~~python
import pysan
asndb = pyasn.pyasn('prefix_as-path.dat')
for ip in ips:
   asn_path,prefix =  asndb.lookup(ip)
   if asn:
      print (ip+"\t"+asn_path)
      # or do whatever process you need on the asn_path
~~~
