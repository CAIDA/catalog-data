~~~json
{
    "id" : "single-radius_measurement_with_scamper",
    "name" : "Single-Radius Measurement with Scamper",
    "description" : "How to use Scamper with Python to execute single-radius measurements",
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
The following is an implementation of the well-known [single-radius](https://catalog.caida.org/paper/2020_ripe_ipmap_active_geolocation) measurement, which conducts delay measurements to an IP address from a distributed set of vantage points, and reports the shortest of all the RTTs obtained with the name of the monitor, which on Ark, is derived from its location (e.g., lax-us, hlz2-nz, ams-nl, and so on). Researchers and operators might use this technique to understand approximately where a system is located, using the RTT constraint of the vantage point that reports the shortest delay.

## Installing Scamper
Links to Scamper packages for various platforms can be found on [Scamper's wesbite](https://www.caida.org/catalog/software/scamper/#scamper-availability); installation procedure depends on which platform you are using. Windows users can use the Ubuntu PPA with [Windows Subsystem for Linux (WSL)](https://ubuntu.com/desktop/wsl).

## Solution
~~~python
import sys
from datetime import timedelta
from scamper import ScamperCtrl

# check parameters:
# - a directory containing unix domain sockets
# - an IP address to probe
if len(sys.argv) != 3:
  print("usage: single-radius.py $dir $ip")
  sys.exit(-1)

# open an interface (ScamperCtrl object)
ctrl = ScamperCtrl(remote_dir=sys.argv[1])

# order a ping measurement from vantage point instances
for i in ctrl.instances():
  ctrl.do_ping(sys.argv[2], inst=i)

# find the smallest RTT among instances
min_rtt = None
min_vp = None
# 10s timeout to ensure that experiment won't 
# be held up if a vantage point experiences outage
for o in ctrl.responses(timeout=timedelta(seconds=10)):
  if o.min_rtt is not None and (min_rtt is None or min_rtt > o.min_rtt):
    min_rtt = o.min_rtt
    min_vp = o.inst

# print the results of the experiment
if min_rtt is not None:
  print(f"{min_vp.name} {(min_rtt.total_seconds()*1000):.1f} ms")
else:
  print(f"no responses for {sys.argv[2]}")
~~~

This implementation takes two parameters -- a directory that contains a set of unix domain sockets, each of which represents an interface to a single vantage point, and an IP address to probe. Then, we open an interface (represented by a ScamperCtrl object) that contains all of the vantage points in that directory. We then send a ping measurement to each of the vantage point instances. These ping measurements operate in parallel -- the ping measurements on each of the nodes operate asynchronously. We then collect the results of the measurements, noting the minimum observed RTT, and the vantage point where it came from. We pass a 10-second timeout so that a vantage point that experiences an outage after we send the measurements does not hold up the whole experiment. Finally, we print the result of the measurement.

## Background
### What is single-radius measurement?
Single-radius measurement is a technique for approximating the location of an IP address based on the latency (delay) of pings to that address from various vantage points. The vantage point whose ping gets the fastest response is likely to be the closest one to the machine with that IP address, so it's thought that the IP address lies within a certain radius of that vantage point. Since a decent approximation can be made with just the nearest vantage point's location and its latency, the other information is discarded, and the measurement consists only of that vantage point's location and a radius based on the latency.

### What is Scamper?
Scamper is a tool for conducting Internet measurements that supports an array of functionalities. More information can be found on [Scamper's website](https://www.caida.org/catalog/software/scamper/).

### How do I use Scamper with Python?
First, Scamper must be installed on your system ([see package information](https://www.caida.org/catalog/software/scamper/#scamper-availability)). Then, the [Python module documentation](https://www.caida.org/catalog/software/scamper/python/) provides detailed instructions on using Python to interact with Scamper processes.