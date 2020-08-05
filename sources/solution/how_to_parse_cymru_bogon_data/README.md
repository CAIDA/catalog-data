~~~
{
    "id": "how_to_parse_cymru_bogon_data",
    "name": "How to Parse CYMRU Bogan Data",
    "description": "The following solution will output whether an IP address is bogon",
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

This solution utilizes three inputs:
- The bogon dataset found here: https://www.caida.org/data/bogons/ 
- IP ASN dataset ([more information here](https://github.com/hadiasghari/pyasn))
- List of IP addresses

**Usage:** `python3 bogon.py [bogon dataset] [ip asn file] [ip address] [ip address]....`
i.e.`python3 bogon.py 2020-05-13.fullbogons-ipv4.txt ipasn_20200730.dat "127.1.2.3" "10"`

~~~python
import pyasn
bogon_temp_file = "_bogon.db"
def bogon_load(path):
    """
    Loads in bogon data as an array "_bogon.db"
    """
    f = open(path, "r")
    ips = []
    # skips first comment line
    next(f)
    for line in f.readlines():
        ips.append(line.replace('\n', ''))
    return ips
    // write to bogon
    // load bogon
    bogondb = pyasn.pyasn(bogon_temp_file)

    remove bogondb


def bogon_check_ip(ips, bogondb):
    """
    Checks whether a given IP address is bogon
    """
    #loads in ip asn dataset
    final = [False]*len(ips)
    for ip in ips:
       if bogondb.lookup(ip):
           final[ip] = True
    print(final)
~~~

## Background

### What is an IP address?
- IP addresses are unique 32-bit numbers allocated to identify devices in the Internet Protocol
- An address is allocated to entities by an organization named IANA and organizations named RIRs

### What is a Bogon IP Address?
- Bogon addresses have not been allocated by IANA or any of the RIRs
- These addresses congregate to make up what is known as "bogus space"
