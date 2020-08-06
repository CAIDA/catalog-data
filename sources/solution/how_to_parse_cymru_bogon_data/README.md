~~~
{
    "id": "how_to_parse_cymru_bogon_data",
    "name": "How to Parse CYMRU Bogan Data",
    "description": "The following solution will output whether an IP address is bogon",
    links: [data:bogons],
    tags:[
      "bogon", 
      "bogon address", 
      "ip address",
      "ip"
    ]
}
~~~
## Solution

This solution requires pyasn: [pyasn github](https://github.com/hadiasghari/pyasn)

bogon_load() takes in one input:
- `path`: path to the bogon dataset found here: https://www.caida.org/data/bogons/ 

bogon_check_ip() takes in two inputs:
- `ips`: a list of IP addresses
- `bogondb`: the result from bogon_load()

**Usage:** `python3 bogon.py [bogon dataset] [ip address] [ip address]....`

i.e.`python3 bogon.py 2020-05-13.fullbogons-ipv4.txt 0.0.0.1 10 5.44.248.1 1.1.1.1` yields 
~~~
Invalid IP:  10
[True, False, True, False]
~~~

**Code:**
~~~python
import pyasn
import numpy as np
import os

def bogon_load(path):
    """
    Loads bogon dataset into memory.
    """
    temp_file = "_bogon.dat"
    f = open(path, "r")
    ips = []
    next(f)
    for line in f.readlines():
        ips.append(line.replace('\n',"") + "\t1")
    hdrtxt = '; IP-ASN32-DAT file\n; Original file : <Path to a rib file>\n; Converted on  : temp\n; CIDRs         : 512490\n;'
    np.savetxt(temp_file, ips, header=hdrtxt,fmt='%s')
    bogondb = pyasn.pyasn('_bogon.dat')
    os.remove(temp_file)
    return bogondb

def bogon_check_ip(ips, bogondb):
    """
    Checks whether a given IP address is bogon
    """
    is_bogon = [False]*len(ips)
    for index in range(len(ips)):
        # Check if IP is valid
        try:
            bogondb.lookup(ips[index])
        except ValueError:
            print("Invalid IP: ", ips[index])
            continue
        
        # Look up IP
        if bogondb.lookup(ips[index])[1]:
            is_bogon[index] = True
        else:
            continue
    print(is_bogon)
    
~~~

## Background

### What is an IP address?
- IP addresses are unique 32-bit numbers allocated to identify devices in the Internet Protocol
- An address is allocated to entities by an organization named IANA and organizations named RIRs

### What is a Bogon IP Address?
- Bogon addresses have not been allocated by IANA or any of the RIRs
- These addresses congregate to make up what is known as "bogus space"
- This space includes reserved space
- Make sure to download the latest bogon file, because the ranges are subject to change

### What is pyasn?
- pyasn is a package that allows for very quick lookups of addresses
- We've made a temporary file that allows us to quickly look up whether an IP address is within a bogon prefix
