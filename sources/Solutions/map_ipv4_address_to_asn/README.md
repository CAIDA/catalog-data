~~~
{
    "question": "How to find the AS path for a IPv4 address with Python?",
    "links": ["dataset:BGPStream"],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools"
    ]
}
~~~
background: 	https://www.geeksforgeeks.org/longest-prefix-matching-in-routers/

# solution
Write a script that uses BGPStream's [PyBGPStream](https://bgpstream.caida.org/docs/tutorials/pybgpstream)
to download and store the AS path and prefixes into prefix-as_paths.dat.  Write a script using
[pyasn](https://pypi.org/project/pyasn/) that loads prefix-as_paths.dat, and then use it to map
between the prefix-as_paths.dat and your ips. Below are the relavent code snippets.

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
