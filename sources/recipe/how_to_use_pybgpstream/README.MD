## How to use PyBGPStream 

~~~json
{
  "name": "How to use PyBGPStream?",
  "description": "Gives a simple example of using PyBGPStream",
  "links": [
    "software:bgpstream"
  ],
  "tags": [
    "measurement methodology",
    "topology",
    "software/tools",
    "asn"
  ],
  "authors":[
        {
            "person": "person:pathak__pooja",
            "organizations": [ "CAIDA, San Diego Supercomputer Center, University of California San Diego" ]
        }
    ]
}
~~~

The following solution provides an in-depth explanation of how to install and use **PyBGPStream** with an example. 

## <ins> Introduction </ins> 
PyBGPStream is a Python library that provides a high-level interface for live and historical BGP data analysis. See http://bgpstream.caida.org for more information about BGPStream. 

PyBGPStream provides two Python modules, `_pybgpstream`, a low-level (almost) direct interface to the [libBGPStream]( https://bgpstream.caida.org/ ) C API, and `pybgpstream`, a high-level 'Pythonic' interface to the functionality provided by `_pybgpstream`. 


## Solution 

The following code snippet demonstrates the use of **PyBGPStream**.\
The script can be found [here]( https://github.com/CAIDA/catalog-data/blob/how_to_use_pybgpstream/sources/solution/how_to_use_pybgspstream/pybgpstream-example.py ).

~~~python

import pybgpstream

# Create PyBGPStream instance 
stream = pybgpstream.BGPStream(
    from_time="2017-07-07 00:00:00", until_time="2017-07-07 00:10:00 UTC",
    collectors=["route-views.sg", "route-views.eqix"],
    record_type="updates",  
)

# This should limit BGPStream to download the full first BGP dump
stream.add_rib_period_filter(86400)

for elem in stream:
    # record fields can be accessed directly from elem
    # print(elem)
    print(elem.fields)
    # {'next-hop': '27.111.228.201', 'as-path': '133165 4637 174 13188', 'communities': {'4637:32502', '4637:32412', '4637:32026', '4637:60952'}, 'prefix': '37.57.179.0/24'}                     
~~~

`elem.fields` returns a dictionary in the following format:
`{'next-hop': '', 'as-path': '', 'communities': {':', ':', ':', ':'}, 'prefix': ''}`

- `next-hop`: The next IP address hop 
- `as-path`: The as path followed by the IP address 
- `communities`: The communities (a set of strings in the canonical “asn:value” format)
- `prefix`: The IP address prefix 

## Using PyBGPStream ##

### Installation ###
To get started using PyBGPStream, first [install libBGPStream]( https://bgpstream.caida.org/docs/install/pybgpstream ).

Then, you should be able to install PyBGPStream using pip: 

~~~
$ pip3 install pybgpstream
~~~ 

Alternatively, to install PyBGPStream from source either clone the [Github repository]( https://github.com/CAIDA/bgpstream
 ) (PyBGPStream is located in the `pybgpstream` subdirectory), or download a [source tarball]( https://bgpstream.caida.org/download ) and then run:

~~~ 
 $ python setup.py build 
 $ python setup.py install
~~~ 

For more information on installing PyBGPStream, please see the detailed [installation instructions]( https://bgpstream.caida.org/docs/install/pybgpstream ) on the BGPStream website. 
 
Please see the [PyBGPStream API documentation]( https://bgpstream.caida.org/docs/api/pybgpstream ) and the [PyBGPStream tutorial]( https://bgpstream.caida.org/docs/tutorials/pybgpstream ) for more information about using PyBGPStream.
 
### Creating a stream ###

The first step in each pybgpstream script is to import the modules and create a BGPStream instance. 

~~~python 
import pybgpstream

stream = pybgpstream.BGPStream(
    from_time="2017-07-07 00:00:00", until_time="2017-07-07 00:10:00 UTC",
    collectors=["route-views.sg", "route-views.eqix"],
    record_type="updates",
    # filter="peer 11666 and prefix more 210.180.0.0/16"
    ) 
~~~

The BGPStream instance contains a few added filters to narrow the stream - 
- **from_time** : Specifies start time of the stream. e.g.`"2017-07-07 00:00:00"`
- **until_time**: Specifies end time of the stream. e.g.`"2017-07-07 00:10:00 UTC"` 
- **collectors**: Narrows the stream to specific collectors. 
- **record_type**: `updates` narrows the stream to only updates (i.e not RIB dumps) 
- **filter**: Specifies flexible filter conditions. More on filters [here]( https://github.com/CAIDA/libbgpstream/blob/master/FILTERING
 )

At this point we can start the stream, and repeatedly ask for new BGP elems. Each time a valid record is read, we extract from it the elems that it contains and print the record and elem fields. If a non-valid record is found, we do not attempt to extract elems.
The code below simply prints all elements in stream.

~~~python 
for elem in stream:
    # record fields can be accessed directly from elem
    # print(elem)
    print(elem.fields)
~~~

If you want to use **PyBGPStream** to
- Map between MOAS ipv4 addresses and their prefixes 
- Measure the extent of AS Path Inflation 
- Find ipv4 addresses associated with certain communities 

View tutorials [here]( https://bgpstream.caida.org/docs/tutorials/pybgpstream). 
 
## Example Script
`pybgpstream-example.py` is a file that shows some features of PyBGPStream, such as printing records and getting ASNs and prefixes.
### Usage
You may want to send printed data from STDOUT to a file to reduce clutter.

~~~ bash
./pybgpstream-example.py > output.txt
~~~

## <ins> Background </ins>  

PyBGPStream is used to extract information from BGP collectors and BGP elems. See more information on BGP collectors [here]( https://learn.nsrc.org/bgp/route_collectors#:~:text=A%20route%20collector%20is%20usually,collector%20does%20not%20forward%20packets.).

### Definitions  
- **Organization** : Each ASN can be mapped to an organization that controls multiple AS's over its network.
- **Customer** : ASes at lower levels are customers who pay ISPs (providers) at higher levels in exchange for access to the rest of the Internet. 
- **Peer** : Peer-to-peer links (p2p) connects two ISPs who have agreed to exchange traffic on a quid pro quo basis. Peers should exchange traffic only between each other and each other's customers.
- **Origin AS**: An IP address and prefix can be traced back to an AS, known as the origin AS.
- **Prefix**: An *IP address prefix* is the prefix of an IPv4 address within a given network. (for example, suppose a network possesses all IPv4 addresses that begin with 172.88., thus 172.88. is the network's prefix. Since each integer in an IPv4 address is 8 bits, this prefix has a length of 16 bits, and would be written: 172.88.0.0/16)

More information on AS relationships can be found [here]( https://asrank.caida.org/about ).

## Caveats 
- The script includes the line `stream.add_rib_period_filter(86400)`
- This limits BGPStream to download the full first BGP dump. 
- More information on `add_rib_period_filter` and other **pybgpstream** methods can be found [here]( https://bgpstream.caida.org/docs/api/pybgpstream/_pybgpstream.html ).
- It may take a few minutes for the program to finish running. 
