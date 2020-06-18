~~~json
{
    "name": "How to get a router's IPs, ASN, neighbors, and geographic location.",
    "description":"Using the ASN's organizatoin's country in WHOIS to map an ASN to the country of it's headquarters.",
    "links": ["dataset:AS_Organization"],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools",
        "ASN",
        "geolocation"
    ]
}
~~~
https://www.caida.org/publications/papers/2012/topocompare-tr/topocompare-tr.pdf
https://www.caida.org/publications/presentations/2016/as_intro_topology_wind/as_intro_topology_wind.pdf
https://www.cs.rutgers.edu/~pxk/352/notes/autonomous_systems.html
https://www.caida.org/data/internet-topology-data-kit/ <--

https://www.caida.org/data/request_user_info_forms/ark.xml (download your copy of data)
https://docs.python.org/3/library/bz2.html
### Introduction ###

midar-iff.nodes.bz2
~~~
node N1:  5.2.116.4 5.2.116.28 5.2.116.66 5.2.116.70 5.2.116.78 5.2.116.88 5.2.116.108 5.2.116.142
~~~

midar-iff.links.bz2
~~~
link L1:  N27677807:1.0.0.1 N106961
~~~

midar-iff.nodes.as.bz2
~~~
node.AS N1 31655 refinement
~~~

midar-iff.nodes.geo.bz
~~~
# node.geo nod_id: continent country region city lat lon population method
node.geo N4:    SA      CO      34      Bogota  4.60971 -74.08175       7674366         ddec
~~~

ecode
~~~json
{
    "id":4,
    "asn":123,
    "ips":["12.3.34"],
     "neighbors":[3,2,3],
    "location":{
        "continent":"SA",
        "country":"CO",
        "region":"34",
        "city"
        ....
     }
}
~~~

useage: parse_ark.py -n nodes.bz2 -l links.bz2 -a nodes.as.bz2 -g nodes.geo.bz2
~~~python
import bz2
with bz2.open(filename) as f:
   for line in f:
      line = line.encode()
~~~
