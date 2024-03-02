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