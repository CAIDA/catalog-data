~~~json
{
    "id" : "authoritative_nameserver_delay_with_scamper",
    "name" : "Measuring Authoritative Nameserver Delay with Scamper",
    "description" : "Using Scamper to measure RTTs to authoritative name servers of a specific domain",
    "links": [
        {"to":"software:scamper"}
    ],
    "tags" : [
        "scamper"
    ],
    "authors":[
        {
            "person": "person:masser-frye__richard",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## Introduction
Let's say we want to know the RTTs (Round Trip Times) to the authoritative nameservers for a given zone from a single vantage point. This script demonstrates how to measure that using Scamper and its associated Python module.

## Installing Scamper
Links to Scamper packages for various platforms can be found on [Scamper's wesbite](https://www.caida.org/catalog/software/scamper/#scamper-availability); installation procedure depends on which platform you are using. Windows users can use the Ubuntu PPA with [Windows Subsystem for Linux (WSL)](https://ubuntu.com/desktop/wsl).

## Solution
~~~python
import sys
from datetime import timedelta
from scamper import ScamperCtrl

# check that two parameters were provided
if len(sys.argv) != 3:
  print("usage: authns-delay.py $vp $zone")
  sys.exit(-1)

# open an interface (ScamperCtrl object) with only 1 vantage point
ctrl = ScamperCtrl(remote=sys.argv[1])

# get the list of nameservers for the zone, synchronously
o = ctrl.do_dns(sys.argv[2], qtype='NS', wait_timeout=1, sync=True)

# issue queries for the IP addresses of the authoritative servers
ns = {}
for rr in o.ans():
  if rr.ns is not None and rr.ns not in ns:
    ns[rr.ns] = 1
    # search for A record (IPv4 address)
    ctrl.do_dns(rr.ns, qtype='A', wait_timeout=1)
    # search for AAAA record (IPv6 address)
    ctrl.do_dns(rr.ns, qtype='AAAA', wait_timeout=1)

# collect the unique addresses out of the address lookups
addr = {}
for o in ctrl.responses(timeout=timedelta(seconds=3)):
  for a in o.ans_addrs():
    addr[a] = o.qname

# collect and print RTTs for the unique IP addresses
for a in addr:
  ctrl.do_ping(a)
for o in ctrl.responses(timeout=timedelta(seconds=10)):
  print(f"{addr[o.dst]} {o.dst} " +
        (f"{(o.min_rtt.total_seconds() * 1000):.1f}"
         if o.min_rtt is not None else "???"))
~~~
This implementation takes two parameters -- a single vantage point, and a zone name to study. As before, we open an interface to that VP, then issue a DNS query for the authoritative nameservers for the zone.

There are a couple of interesting things to note about the call to `do_dns`. First, we do not pass a handle representing the VP instance to the `do_dns` method, as the ScamperCtrl interface only has a single instance associated with it -- it is smart enough to use that single instance for the measurement. Second, we pass `sync=True` to make the measurement synchronous -- the method does not return until it has the results of that single measurement. This is shorter (in lines of code) and more readable than issuing an asynchronous measurement and then collecting the single result. Then, we issue asynchronous queries for the IPv4 and IPv6 addresses for the nameservers returned and send ping measurements for each of the addresses. Finally, we print the names of the nameservers, their IP addresses, and the minimum RTT observed to each.

## Background
### What is an authoritative nameserver?
When resolving a domain name (like google.com) into an IP address, a computer begins by querying a DNS root server, which directs it to a TLD server (specific to the URL's ending, like .com or .net) which then directs it to an authoritative nameserver, which will have the most specific information about that domain name. Authoritative nameservers take domains as queries and return information like IP addresses.

### What is a zone?
A DNS zone is a set of domains managed by a single individual or organization.