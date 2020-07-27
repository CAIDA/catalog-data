## How to use PyBGPStream ##
~~~
{
    "name": "How to use PyBGPStream?",
    "descriptions": "Gives a simple example of using PyBGPStream"
    "links": ["software:bgpstream"],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools",
        "asn",
    ]
}
~~~

The following solution provides an in-depth explanation of how to install and use **PyBGPStream** with an example. 

 ## Introduction ##
PyBGPStream is a Python library that provides a high-level interface for live and historical BGP data analysis. See http://bgpstream.caida.org for more information about BGPStream. 

PyBGPStream provides two Python modules, `_pybgpstream`, a low-level (almost) direct interface to the [libBGPStream]( https://bgpstream.caida.org/ ) C API, and `pybgpstream`, a high-level 'Pythonic' interface to the functionality provided by `_pybgpstream`. 


### Solution ###

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
`elem.fields` returns a dictionary in the following format: \
`{'next-hop': '', 'as-path': '', 'communities': {':', ':', ':', ':'}, 'prefix': ''}`

• `next-hop`: The next IP address hop \
• `as-path`: The as path followed by the IP address \
• `communities`: The communities (a set of strings in the canonical “asn:value” format)\
• `prefix`: The IP address prefix 


## Background ##

 ### Installation ###
To get started using PyBGPStream, first [install libBGPStream]( https://bgpstream.caida.org/docs/install/pybgpstream ).

Then, you should be able to install PyBGPStream using pip: 

`$ pip install pybgpstream `

Alternatively, to install PyBGPStream from source either clone the [Github repository]( https://github.com/CAIDA/bgpstream
 ) (PyBGPStream is located in the `pybgpstream` subdirectory), or download a [source tarball]( https://bgpstream.caida.org/download ) and then run:
 
 `$ python setup.py build`\
 `$ python setup.py install`
 
 For more information on installing PyBGPStream, please see the detailed [installation instructions]( https://bgpstream.caida.org/docs/install/pybgpstream ) on the BGPStream website. 
 
 Please see the [PyBGPStream API documentation]( https://bgpstream.caida.org/docs/api/pybgpstream ) and the [PyBGPStream tutorial]( https://bgpstream.caida.org/docs/tutorials/pybgpstream ) for more information about using PyBGPStream.
 
 ### Explanation ###
 
• PyBGPStream is used to extract information from BGP collectors and BGP elems. See more information on BGP collectors [here]( https://learn.nsrc.org/bgp/route_collectors#:~:text=A%20route%20collector%20is%20usually,collector%20does%20not%20forward%20packets.)

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

The BGPStream instance contains a few added filters to narrow the stream - \
• **from_time** : Specifies start time of the stream. `"2017-07-07 00:00:00"`\
• **until_time**: Specifies end time of the stream. `"2017-07-07 00:10:00 UTC"` \
• **collectors**: Narrows the stream to specific collectors. \
• **record_type**: `updates` narrows the stream to only updates (i.e not RIB dumps) \
• **filter**: Specifies flexible filter conditions. More on filters [here]( https://github.com/CAIDA/libbgpstream/blob/master/FILTERING
 )

At this point we can start the stream, and repeatedly ask for new BGP elems. Each time a valid record is read, we extract from it the elems that it contains and print the record and elem fields. If a non-valid record is found, we do not attempt to extract elems.

~~~python 
for elem in stream:
    # record fields can be accessed directly from elem
    # print(elem)
    print(elem.fields)
~~~

**PyBGPStream** can be used to - \
• Map between MOAS ipv4 addresses and their prefixes \
• Measure the extent of AS Path Inflation \
• Find ipv4 addresses associated with certain communities 

These scripts can be found [here]( https://bgpstream.caida.org/docs/tutorials/pybgpstream
 ). 
 
 
 ## Caveats ## 
