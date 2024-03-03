import sys
from datetime import timedelta
from scamper import ScamperCtrl

if len(sys.argv) != 3:
  print("usage: authns-delay.py $vp $zone")
  sys.exit(-1)

ctrl = ScamperCtrl(remote=sys.argv[1])

# get the list of NS for the zone
o = ctrl.do_dns(sys.argv[2], qtype='NS', wait_timeout=1, sync=True)

# issue queries for the IP addresses of the authoritative servers
ns = {}
for rr in o.ans():
  if rr.ns is not None and rr.ns not in ns:
    ns[rr.ns] = 1
    ctrl.do_dns(rr.ns, qtype='A', wait_timeout=1)
    ctrl.do_dns(rr.ns, qtype='AAAA', wait_timeout=1)

# collect the unique addresses out of the address lookups
addr = {}
for o in ctrl.responses(timeout=timedelta(seconds=3)):
  for a in o.ans_addrs():
    addr[a] = o.qname

# collect RTTs for the unique IP addresses
for a in addr:
  ctrl.do_ping(a)
for o in ctrl.responses(timeout=timedelta(seconds=10)):
  print(f"{addr[o.dst]} {o.dst} " +
        (f"{(o.min_rtt.total_seconds() * 1000):.1f}"
         if o.min_rtt is not None else "???"))