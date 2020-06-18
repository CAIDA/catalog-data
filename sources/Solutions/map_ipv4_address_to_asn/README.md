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
background: 	https://www.geeksforgeeks.org/longest-prefix-matching-in-routers/

~~~
10.2.1.0/24  10 2 3 5  5
10.2.1.0/24  23 5      5
10.2.1.0/24  23 4 5    5
10.2.1.0/24  21 8 4    4
10.2.1.0/24  21 8 {4,3}   as set

10.2.1.0/24 4_5 multie origi
10.2.1.0/24  4_{4,3}
~~~

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
