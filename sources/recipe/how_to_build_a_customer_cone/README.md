~~~json
{
    "id" : "how_to_build_a_customer_cone",
    "name" : "How to build a Customer Cone with BGPStream.",
    "description" : "How to build ASN Customer Cone using AS Relationship data and BGPStream.",
    "links": [
        {"to":"dataset:as_relationships_serial_1"},
        {"to":"software:bgpstream"}
    ],
    "tags" : [
        "asn",
        "spoofer"
    ],
    "authors":[
        {
            "person": "person:huffaker__bradley",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## Introduction

This program provides an implementation for inferring the <a href="https://asrank.caida.org/about#cone">AS customer cone</a>
using <a href="https://bgpstream.caida.org/">BGPStream</a> and <a href="https://www.caida.org/catalog/datasets/as-relationships/">AS
Relationships</a>.

## Background

The Internet is composed of thousands of ISPs that operate individual parts of the Internet infrastructure. 
ISPs engage in both formal and informal relationships to collectively and ubiquitously route traffic in the Internet. 
These relationships are usually realized in the form of business agreements that translate into engineering constraints 
on traffic flows within and across individual networks participating in the global Internet routing system.
ISP represent their network in the Internet as 
<a href="https://en.wikipedia.org/wiki/Autonomous_system_%28Internet%29">Autonomous Systems (AS)</a>.

<a href="https://en.wikipedia.org/wiki/Routing_table#:~:text=In%20computer%20networking%2C%20a%20routing,distances)%20associated%20with%20those%20routes.">RIB (Routing Information Base)</a> 
is a file that stores route from one router/network host to other destinations on the internet.

<a href="http://www.routeviews.org/routeviews/">Routeview</a> collects real-time BGP information of internet worldwide.
BGP is the routing protocol of the network of ASes, allowing autonomous systems to communicate with one another. This program will 
collect RIB information through the Routeview project.

<a href="https://www.ripe.net/">RIPE NCC</a> is the "Regional Internet Registry in Europe, Middle East, and Parts of Central Asia"
that allocates and registers blocks of ASNs to ISPs and organizations.  


Although business agreements between ISPs can be complicated, the original model introduced by Gao 1 abstracts business relationships 
into the following two most common types:

 1. **customer-to-provider**: a customer pays its provider for transit
 1. **peer-to-peer (p2p)**: two peers exchange transit without paying



By examining the set of ASes an AS can reach through its customers, we can see the scope of 
its customer base and compare AS "sizes". We defined this set of ASes as its <a href="https://www.caida.org/catalog/papers/2013_asrank/asrank.pdf">
customer cone</a> (set of ASes an AS can reach through customer links).
Take in the AS path and crop it to the first peer-to-peer or provider-to-customer link.
For every AS that follows an ASN in the path, include that ASN in that AS's customer cone.

~~~
    asn__cone
    stream = BGPStream(
        from_time=from_time.strftime("%Y-%m-%d %H:%M:%S"), until_time=until_time.strftime("%Y-%m-%d %H:%M:%S"),
        record_type="ribs"
    )
    stream.add_rib_period_filter(86400) # This should limit BGPStream to download the full first BGP dump

    for elem in stream:
        asns = elem.fields['as-path'].split(" ")

        # Skip until the first peer-peer or provider->customer link
        i = 0
        while i+1 < len(asns):
            link = asns[i]+" "+asns[i+1] 
            i += 1
            if link in peer_provider:
                break

        # Since an AS only announces it's customer cone to it's peer or provider,
        # the remaining ASes in the path are in the preciding ASes customer cone.
        while i+1 < len(asns):
            if asns[i] not in asn__cone:
                asn__cone[asns[i]] = set()
            cone = asn__cone[asns[i]]
            j = i+1
            while j < len(asns):
                print (">",i,j,asns[i], asns[j])
                cone.add(asns[j])
                j += 1
            i += 1
~~~


## Instructions

1. download /datasets/as-relationships/serial-1/20220701.as-rel.txt.bz2 from 
<a href="https://www.caida.org/catalog/datasets/as-relationships/">AS Relationships</a>.
2. install <a href="https://bgpstream.caida.org/v2-whats-new"> BGP Stream </a>. If your device runs Windows, follow the instructions in [How to install BGPStream on Windows](https://placeholderlink.net).
3. Then run ``python2 build-cone.py [-d N] 20220701.as-rel.txt.bz2 > asn_cones.txt``
   (The optional ``-d`` debug option specifies program to process N traces to shorten execution time).
   This program runs on Python 2.7


   sample output
   ~~~
   # the following line means that AS 132's customer cone include AS 35 and AS 2.
   132 35 2
   ~~~


## Caveats

It is important to point out that this will not produce exactly the same result as 
you would find on asrank.caida.org.  This is because AS Rank filters the incoming 
path to remove poisoned paths, Internet eXchange Points, and loops.  This effect
only a small number of paths, so the differences will not be large.

You can ignore: "WARN: NOT_IMPLEMENTED: BGP UPDATE Path Attribute 255 is not yet implemented (parsebgp_bgp_update.c:554)"

This program collects RIB of the entire internet, therefore it will take very long to run, and we decided to only
include RIB data for one second (first second of yesterday). Make sure to reserve >100GB of disk space before executing the program.


We strongly recommend the debug option for a brief overview of the program. 


Copyright (c) 2023 The Regents of the University of California
All Rights Reserved