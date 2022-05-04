# How to find an ASN's summarized spoofing status

~~~json
{
    "id" : "how_to_find_an_asns_summarized_spoofing_status",
    "name" : "How to find an ASN's summarized spoofing status",
    "description" : "Directions to Spoofer web pages which show spoofing status",
    "links": [
        {"to":"software:spoofer_ui"}
    ],
    "tags" : [
        "security",
        "spoofer"
    ],
    "authors":[
        {
            "person": "person:koga__ryan",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

The Spoofer web pages present multiple different summaries of spoofing results.  <https://spoofer.caida.org/as_stats.php> shows a top-level view of all the ASNs where Spoofer tests were run within the last year.  Clicking on any of the listed ASNs will give a more detailed page showing the spoofing status broken down by IP block (/24 for IPv4 and /40 for IPv6).  For example, <https://spoofer.caida.org/as.php?asn=7922> shows many IP blocks, some of which have seen evidence of spoofing and some of which haven't.  These blocks are by default sorted by spoofing status, but can also be sorted by any of the column headers.

## Background

### What is IP spoofing?
IP spoofing is the practice of forging various portions of the Internet Protocol (IP) header. Because a vast majority of Internet traffic, applications, and servers use IP, IP spoofing has important security implications.

### What is this project?

The Spoofer Project seeks to understand the Internet's vulnerability to different types of spoofed-source IP address attacks.  The Spoofer client program attempts to send a series of spoofed UDP packets to servers distributed throughout the world. These packets are designed to test:

* Different classes of spoofed IPv4 and IPv6 addresses, including private and routable
* Ability to spoof neighboring, adjacent addresses
* Ability to spoof inbound (towards the client) and outbound (from the client)
* Where along the path filtering is observed
* Presence of a NAT device along the path

### Where can I learn more?

FAQ:  https://www.caida.org/projects/spoofer/faq
