# key/values
- question: 
   - How do you map an IPv4 address to an ASN path in Python?
- datasets:
   - dataset: BGPStream
     - joins: [["AS Path IPv4","Prefix IPv4"]]
- topics: 
   - measurement methdology
   - topology
   - software/tools
# solution
Write a script that uses BGPStream's [PyBGPStream](https://bgpstream.caida.org/docs/tutorials/pybgpstream)
to download and store the AS path and prefixes into prefix-as_paths.dat.  Write a script using
[pyasn](https://pypi.org/project/pyasn/) that loads prefix-as_paths.dat, and then use it to map
between the prefix-as_paths.dat and your ips. Below are the relavent code snippets.

##### BGPStream
~~~
#!/usr/bin/env python

import pybgpstream
stream = pybgpstream.BGPStream(
    from_time="2017-07-07 00:00:00", until_time="2017-07-07 00:10:00 UTC",
    collectors=["route-views.sg", "route-views.eqix"],
    record_type="updates",
    filter="peer 11666 and prefix more 210.180.0.0/16"
)

for elem in stream:
    # record fields can be accessed directly from elem
    # e.g. elem.time
    # or via elem.record
    # e.g. elem.record.time
    asn_path = elem.fields["as-path"]
    prefix = elem.fields["prefix"]
    print(prefix+"\t"+asn_path)
~~~

##### pyasn
~~~
asndb = pyasn.pyasn('prefix_as-path.dat')

for ip in ips:
   asn_path,prefix =  asndb.lookup(ip)
   if asn:
     print (ip+"\t"+asn_path)
     # or do whatever process you need on the asn_path
~~~
